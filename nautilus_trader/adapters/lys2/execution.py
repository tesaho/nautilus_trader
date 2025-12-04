# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------
"""
Execution client for the Lys adapter.
"""

import asyncio
import json
from decimal import Decimal
from typing import Any

from nautilus_lys2 import LysZmqClient

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import MessageBus
from nautilus_trader.common.enums import LogColor
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.execution.messages import CancelOrder
from nautilus_trader.execution.messages import ModifyOrder
from nautilus_trader.execution.messages import SubmitOrder
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.live.execution_client import LiveExecutionClient
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OmsType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import ClientOrderId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TradeId
from nautilus_trader.model.identifiers import VenueOrderId
from nautilus_trader.model.objects import AccountBalance
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Quantity

from nautilus_trader.adapters.lys2.config import LysExecClientConfig
from nautilus_trader.adapters.lys2.constants import LYS_CLIENT_ID
from nautilus_trader.adapters.lys2.constants import LYS_VENUE
from nautilus_trader.adapters.lys2.constants import LYS_ZMQ_DEFAULT_IPC
from nautilus_trader.adapters.lys2.constants import LYS_ZMQ_DEFAULT_TCP
from nautilus_trader.adapters.lys2.constants import LAMPORTS_PER_SOL


class LysExecutionClient(LiveExecutionClient):
    """
    Provides an execution client for Lys (Solana transaction execution).

    Parameters
    ----------
    loop : asyncio.AbstractEventLoop
        The event loop for the client.
    client : LysZmqClient
        The Lys ZMQ client.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : LiveClock
        The clock for the client.
    config : LysExecClientConfig
        The configuration for the client.

    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        client: LysZmqClient,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        config: LysExecClientConfig,
    ) -> None:
        super().__init__(
            loop=loop,
            client_id=LYS_CLIENT_ID,
            venue=LYS_VENUE,
            oms_type=OmsType.NETTING,  # Solana uses netting model
            instrument_provider=None,  # Will be set externally if needed
            account_type=AccountType.CASH,  # Solana accounts are cash-based
            base_currency=Currency.from_str("SOL"),
            msgbus=msgbus,
            cache=cache,
            clock=clock,
        )

        self._client = client
        self._config = config
        self._wallet_address: str | None = None
        self._is_connected = False

        # Track pending orders
        self._pending_orders: dict[ClientOrderId, SubmitOrder] = {}

    async def _connect(self) -> None:
        """Connect to the ZMQ client."""
        self._log.info("Connecting to Lys ZMQ client", LogColor.BLUE)

        try:
            # For ZMQ, connection is implicit when sending messages
            # Just verify we have the client ready
            if not self._client:
                msg = "LysZmqClient is not initialized"
                raise RuntimeError(msg)

            self._is_connected = True
            self._log.info("Connected to Lys ZMQ client", LogColor.GREEN)

        except Exception as e:
            self._log.error(f"Failed to connect to Lys ZMQ client: {e}")
            raise

    async def _disconnect(self) -> None:
        """Disconnect from the ZMQ client."""
        self._log.info("Disconnecting from Lys ZMQ client", LogColor.BLUE)

        self._is_connected = False
        self._pending_orders.clear()

        self._log.info("Disconnected from Lys ZMQ client", LogColor.GREEN)

    # -------------------------------------------------------------------------
    # Order execution methods
    # -------------------------------------------------------------------------

    async def _submit_order(self, command: SubmitOrder) -> None:
        """
        Submit an order to Lys for execution.

        Parameters
        ----------
        command : SubmitOrder
            The order submission command.

        """
        try:
            order = command.order

            # Store pending order
            self._pending_orders[order.client_order_id] = command

            # Convert Nautilus order to Lys transaction request
            request = self._create_transaction_request(order)

            self._log.info(
                f"Submitting order {order.client_order_id}: {request}",
                LogColor.BLUE,
            )

            # Execute transaction via ZMQ
            response_json = await self._client.execute_transaction(json.dumps(request))
            response = json.loads(response_json)

            # Handle response
            if response.get("success"):
                signature = response.get("signature", "")
                await self._handle_order_accepted(order, signature)
            else:
                error_msg = response.get("error", "Unknown error")
                await self._handle_order_rejected(order, error_msg)

        except Exception as e:
            self._log.error(f"Error submitting order: {e}")
            await self._handle_order_rejected(order, str(e))

    async def _submit_order_list(self, command: Any) -> None:
        """Submit a list of orders."""
        # Not applicable for Lys - submit orders individually
        self._log.warning("Order list submission not supported for Lys")

    async def _modify_order(self, command: ModifyOrder) -> None:
        """
        Modify an existing order.

        Parameters
        ----------
        command : ModifyOrder
            The order modification command.

        """
        # Solana transactions are atomic and cannot be modified
        # Would need to cancel and resubmit
        self._log.warning(
            f"Order modification not supported for Lys: {command.client_order_id}",
        )

        # Generate modify rejected event
        self.generate_order_modify_rejected(
            strategy_id=command.strategy_id,
            instrument_id=command.instrument_id,
            client_order_id=command.client_order_id,
            venue_order_id=command.venue_order_id,
            reason="Order modification not supported on Solana",
            ts_event=self._clock.timestamp_ns(),
        )

    async def _cancel_order(self, command: CancelOrder) -> None:
        """
        Cancel an existing order.

        Parameters
        ----------
        command : CancelOrder
            The order cancellation command.

        """
        # Solana transactions are atomic and cannot be cancelled once submitted
        # Only pending orders can be removed from tracking
        self._log.warning(
            f"Order cancellation not supported for Lys: {command.client_order_id}",
        )

        # Remove from pending if not yet submitted
        if command.client_order_id in self._pending_orders:
            del self._pending_orders[command.client_order_id]

        # Generate cancel rejected event
        self.generate_order_cancel_rejected(
            strategy_id=command.strategy_id,
            instrument_id=command.instrument_id,
            client_order_id=command.client_order_id,
            venue_order_id=command.venue_order_id,
            reason="Order cancellation not supported on Solana",
            ts_event=self._clock.timestamp_ns(),
        )

    async def _cancel_all_orders(self, command: Any) -> None:
        """Cancel all orders."""
        self._log.warning("Bulk order cancellation not supported for Lys")

    # -------------------------------------------------------------------------
    # Account and position queries
    # -------------------------------------------------------------------------

    async def generate_order_status_report(
        self,
        instrument_id: InstrumentId,
        client_order_id: ClientOrderId | None = None,
        venue_order_id: VenueOrderId | None = None,
    ) -> OrderStatusReport | None:
        """
        Generate an order status report.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the order.
        client_order_id : ClientOrderId, optional
            The client order ID.
        venue_order_id : VenueOrderId, optional
            The venue order ID.

        Returns
        -------
        OrderStatusReport | None
            The order status report if available.

        """
        # Solana transactions are atomic - no ongoing order status
        # Would need to query blockchain for transaction status by signature
        self._log.debug(f"Order status query not implemented for {instrument_id}")
        return None

    async def generate_order_status_reports(
        self,
        instrument_id: InstrumentId | None = None,
        start: Any | None = None,
        end: Any | None = None,
        open_only: bool = False,
    ) -> list[OrderStatusReport]:
        """
        Generate order status reports.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument ID to filter by.
        start : Any, optional
            The start time filter.
        end : Any, optional
            The end time filter.
        open_only : bool, default False
            Whether to only return open orders.

        Returns
        -------
        list[OrderStatusReport]
            The list of order status reports.

        """
        # Would need to query blockchain transaction history
        self._log.debug("Order status reports query not implemented")
        return []

    async def generate_fill_reports(
        self,
        instrument_id: InstrumentId | None = None,
        venue_order_id: VenueOrderId | None = None,
        start: Any | None = None,
        end: Any | None = None,
    ) -> list[Any]:
        """
        Generate fill reports.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument ID to filter by.
        venue_order_id : VenueOrderId, optional
            The venue order ID to filter by.
        start : Any, optional
            The start time filter.
        end : Any, optional
            The end time filter.

        Returns
        -------
        list[Any]
            The list of fill reports.

        """
        # Would need to parse Solana transaction logs
        self._log.debug("Fill reports query not implemented")
        return []

    async def generate_position_status_reports(
        self,
        instrument_id: InstrumentId | None = None,
        start: Any | None = None,
        end: Any | None = None,
    ) -> list[PositionStatusReport]:
        """
        Generate position status reports.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument ID to filter by.
        start : Any, optional
            The start time filter.
        end : Any, optional
            The end time filter.

        Returns
        -------
        list[PositionStatusReport]
            The list of position status reports.

        """
        # Would need to query Solana token accounts
        self._log.debug("Position status reports query not implemented")
        return []

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------

    def _create_transaction_request(self, order: Any) -> dict[str, Any]:
        """
        Create a Lys transaction request from a Nautilus order.

        Parameters
        ----------
        order : Any
            The Nautilus order.

        Returns
        -------
        dict[str, Any]
            The Lys transaction request.

        """
        # Determine execution type and event type from order
        # This is simplified - real implementation would parse instrument ID
        # to determine if it's Pump.fun, Raydium, Jupiter, etc.

        execution_type = "PUMP_FUN"  # Default, should be determined from instrument
        event_type = "BUY" if order.side == OrderSide.BUY else "SELL"

        # Convert order quantity to Solana amounts
        # This is simplified - real implementation would need proper conversions
        sol_amount = int(float(order.quantity) * LAMPORTS_PER_SOL)
        token_amount = int(float(order.quantity) * 1000)  # Placeholder conversion

        # Get fee payer from wallet address or config
        fee_payer = self._wallet_address or self._config.api_key[:44]  # Placeholder

        request = {
            "executionType": execution_type,
            "eventType": event_type,
            "solAmountIn": sol_amount,
            "tokenAmountOut": token_amount,
            "feePayer": fee_payer,
            "priorityFeeLamports": 5000,  # Default priority fee
            "bribeLamports": 0,  # No bribe by default
            "transport": "STANDARD",  # Default transport mode
            "tokenMint": None,  # Should be extracted from instrument ID
        }

        # Add token mint if available from instrument ID
        # Format: TOKEN_SYMBOL.LYS or MINT_ADDRESS.LYS
        if hasattr(order.instrument_id, "symbol"):
            symbol_parts = order.instrument_id.symbol.value.split(".")
            if len(symbol_parts) > 0:
                request["tokenMint"] = symbol_parts[0]

        return request

    async def _handle_order_accepted(self, order: Any, signature: str) -> None:
        """
        Handle an accepted order.

        Parameters
        ----------
        order : Any
            The order that was accepted.
        signature : str
            The Solana transaction signature.

        """
        self._log.info(
            f"Order {order.client_order_id} accepted with signature {signature}",
            LogColor.GREEN,
        )

        # Generate order accepted event
        venue_order_id = VenueOrderId(signature)  # Use signature as venue order ID

        self.generate_order_accepted(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            venue_order_id=venue_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

        # For Solana, transactions are atomic - immediately mark as filled
        # In a real implementation, we would query the transaction to get actual fill details
        self.generate_order_filled(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            venue_order_id=venue_order_id,
            venue_position_id=None,  # Solana doesn't have position IDs
            trade_id=TradeId(signature),
            order_side=order.side,
            order_type=order.order_type,
            last_qty=order.quantity,
            last_px=order.price if hasattr(order, "price") else order.trigger_price,
            quote_currency=Currency.from_str("SOL"),
            commission=Money(0, Currency.from_str("SOL")),  # Would need to calculate from tx
            liquidity_side=LiquiditySide.TAKER,  # Solana DEXes are typically taker
            ts_event=self._clock.timestamp_ns(),
        )

        # Remove from pending
        if order.client_order_id in self._pending_orders:
            del self._pending_orders[order.client_order_id]

    async def _handle_order_rejected(self, order: Any, reason: str) -> None:
        """
        Handle a rejected order.

        Parameters
        ----------
        order : Any
            The order that was rejected.
        reason : str
            The rejection reason.

        """
        self._log.error(
            f"Order {order.client_order_id} rejected: {reason}",
            LogColor.RED,
        )

        # Generate order rejected event
        self.generate_order_rejected(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            reason=reason,
            ts_event=self._clock.timestamp_ns(),
        )

        # Remove from pending
        if order.client_order_id in self._pending_orders:
            del self._pending_orders[order.client_order_id]

    def set_wallet_address(self, address: str) -> None:
        """
        Set the wallet address for transaction signing.

        Parameters
        ----------
        address : str
            The Solana wallet address.

        """
        self._wallet_address = address
        self._log.info(f"Wallet address set: {address}")
