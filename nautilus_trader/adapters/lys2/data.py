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
Data client for the Lys adapter.
"""

import asyncio
import json
from typing import Any

from nautilus_lys2 import LysWebSocketClient

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import MessageBus
from nautilus_trader.common.enums import LogColor
from nautilus_trader.core.nautilus_pyo3 import DataType
from nautilus_trader.live.data_client import LiveMarketDataClient
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import InstrumentId

from nautilus_trader.adapters.lys2.config import LysDataClientConfig
from nautilus_trader.adapters.lys2.constants import LYS_CLIENT_ID
from nautilus_trader.adapters.lys2.constants import LYS_WS_MAINNET_URL
from nautilus_trader.adapters.lys2.constants import LYS_WS_DEVNET_URL


class LysDataClient(LiveMarketDataClient):
    """
    Provides a data client for Lys (Solana real-time transaction monitoring).

    Parameters
    ----------
    loop : asyncio.AbstractEventLoop
        The event loop for the client.
    client : LysWebSocketClient
        The Lys WebSocket client.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : LiveClock
        The clock for the client.
    config : LysDataClientConfig
        The configuration for the client.

    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        client: LysWebSocketClient,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        config: LysDataClientConfig,
    ) -> None:
        super().__init__(
            loop=loop,
            client_id=LYS_CLIENT_ID,
            venue=None,  # Lys is a Solana monitor, not a traditional venue
            msgbus=msgbus,
            cache=cache,
            clock=clock,
        )

        self._client = client
        self._config = config
        self._ws_task: asyncio.Task | None = None
        self._is_running = False

    async def _connect(self) -> None:
        """Connect to the WebSocket server."""
        self._log.info("Connecting to Lys WebSocket", LogColor.BLUE)

        try:
            # Connect returns the receiver stream
            stream = await self._client.connect()

            # Start message processing task
            self._ws_task = self._loop.create_task(self._process_messages(stream))

            # Subscribe to transactions
            await self._client.subscribe_transactions()

            self._is_running = True
            self._log.info("Connected to Lys WebSocket", LogColor.GREEN)

        except Exception as e:
            self._log.error(f"Failed to connect to Lys WebSocket: {e}")
            raise

    async def _disconnect(self) -> None:
        """Disconnect from the WebSocket server."""
        self._log.info("Disconnecting from Lys WebSocket", LogColor.BLUE)

        self._is_running = False

        # Cancel message processing task
        if self._ws_task and not self._ws_task.done():
            self._ws_task.cancel()
            try:
                await self._ws_task
            except asyncio.CancelledError:
                pass

        # Disconnect WebSocket
        try:
            await self._client.disconnect()
        except Exception as e:
            self._log.error(f"Error disconnecting: {e}")

        self._log.info("Disconnected from Lys WebSocket", LogColor.GREEN)

    async def _process_messages(self, stream: Any) -> None:
        """
        Process incoming WebSocket messages.

        Parameters
        ----------
        stream : Any
            The WebSocket message stream.

        """
        self._log.info("Starting message processing", LogColor.BLUE)

        try:
            # The stream is a SplitStream from Rust WebSocket
            # Messages need to be received through the stream
            while self._is_running:
                # Since this is called from Rust, we'll handle it differently
                # For now, just keep the task alive
                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            self._log.info("Message processing cancelled")
        except Exception as e:
            self._log.error(f"Error processing messages: {e}")

    def _handle_transaction_message(self, msg: dict[str, Any]) -> None:
        """
        Handle a transaction message from Lys.

        Parameters
        ----------
        msg : dict[str, Any]
            The parsed transaction message.

        """
        try:
            msg_type = msg.get("type")

            if msg_type == "transaction":
                signature = msg.get("signature", "")
                timestamp = msg.get("timestamp", 0)

                self._log.debug(
                    f"Transaction: {signature} at {timestamp}",
                    LogColor.CYAN,
                )

                # Here you would transform the Solana transaction
                # into Nautilus data types and publish to message bus
                # For example: TradeTick, custom Data, etc.

            elif msg_type == "info":
                message = msg.get("message", "")
                self._log.info(f"Lys info: {message}")

            elif msg_type == "error":
                message = msg.get("message", "Unknown error")
                self._log.error(f"Lys error: {message}")

        except Exception as e:
            self._log.error(f"Error handling transaction message: {e}")

    # Required abstract method implementations

    async def _subscribe_instruments(self) -> None:
        """Subscribe to instrument updates."""
        # Not applicable for Lys - instruments are Solana tokens
        pass

    async def _subscribe_instrument(self, instrument_id: InstrumentId) -> None:
        """Subscribe to a specific instrument."""
        # Not applicable for Lys - subscription is transaction-based
        pass

    async def _subscribe_order_book_deltas(
        self,
        instrument_id: InstrumentId,
        book_type: Any,
        depth: int | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Subscribe to order book deltas."""
        # Not applicable for Lys
        pass

    async def _subscribe_order_book_snapshots(
        self,
        instrument_id: InstrumentId,
        book_type: Any,
        depth: int | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Subscribe to order book snapshots."""
        # Not applicable for Lys
        pass

    async def _subscribe_ticker(self, instrument_id: InstrumentId) -> None:
        """Subscribe to ticker updates."""
        # Not applicable for Lys
        pass

    async def _subscribe_quote_ticks(self, instrument_id: InstrumentId) -> None:
        """Subscribe to quote ticks."""
        # Not applicable for Lys
        pass

    async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
        """Subscribe to trade ticks."""
        # Lys provides Solana transaction data which can be converted to trade ticks
        self._log.info(f"Subscribing to trade ticks for {instrument_id}")
        # Transaction stream already subscribed in _connect()

    async def _subscribe_bars(self, bar_type: Any) -> None:
        """Subscribe to bars."""
        # Not applicable for Lys
        pass

    async def _subscribe_instrument_status(self, instrument_id: InstrumentId) -> None:
        """Subscribe to instrument status updates."""
        # Not applicable for Lys
        pass

    async def _subscribe_instrument_close(self, instrument_id: InstrumentId) -> None:
        """Subscribe to instrument close prices."""
        # Not applicable for Lys
        pass

    async def _unsubscribe_instruments(self) -> None:
        """Unsubscribe from instrument updates."""
        pass

    async def _unsubscribe_instrument(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from a specific instrument."""
        pass

    async def _unsubscribe_order_book_deltas(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from order book deltas."""
        pass

    async def _unsubscribe_order_book_snapshots(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from order book snapshots."""
        pass

    async def _unsubscribe_ticker(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from ticker updates."""
        pass

    async def _unsubscribe_quote_ticks(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from quote ticks."""
        pass

    async def _unsubscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from trade ticks."""
        self._log.info(f"Unsubscribing from trade ticks for {instrument_id}")

    async def _unsubscribe_bars(self, bar_type: Any) -> None:
        """Unsubscribe from bars."""
        pass

    async def _unsubscribe_instrument_status(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from instrument status updates."""
        pass

    async def _unsubscribe_instrument_close(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from instrument close prices."""
        pass

    async def _request_instrument(
        self,
        instrument_id: InstrumentId,
        correlation_id: Any,
        start: Any | None = None,
        end: Any | None = None,
    ) -> None:
        """Request instrument data."""
        pass

    async def _request_instruments(
        self,
        correlation_id: Any,
        start: Any | None = None,
        end: Any | None = None,
    ) -> None:
        """Request instruments data."""
        pass

    async def _request_quote_ticks(
        self,
        instrument_id: InstrumentId,
        limit: int,
        correlation_id: Any,
        start: Any | None = None,
        end: Any | None = None,
    ) -> None:
        """Request historical quote ticks."""
        pass

    async def _request_trade_ticks(
        self,
        instrument_id: InstrumentId,
        limit: int,
        correlation_id: Any,
        start: Any | None = None,
        end: Any | None = None,
    ) -> None:
        """Request historical trade ticks."""
        pass

    async def _request_bars(
        self,
        bar_type: Any,
        limit: int,
        correlation_id: Any,
        start: Any | None = None,
        end: Any | None = None,
    ) -> None:
        """Request historical bars."""
        pass
