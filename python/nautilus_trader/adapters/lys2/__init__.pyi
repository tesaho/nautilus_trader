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
Type stubs for the nautilus_lys2 Rust extension module.

This file provides type hints for IDE support and type checking of the
Rust-based Lys adapter components exposed through PyO3 bindings.
"""

from enum import Enum
from typing import Any

class LysExecutionType(Enum):
    """
    Lys execution type enumeration.

    Represents the type of Solana program to interact with for transaction execution.
    """

    PUMP_FUN: int
    """Pump.fun token operations."""

    RAYDIUM: int
    """Raydium DEX operations."""

    JUPITER: int
    """Jupiter aggregator operations."""

    CUSTOM: int
    """Generic Solana program interaction."""

class LysEventType(Enum):
    """
    Lys event type enumeration.

    Represents the type of trading event (buy or sell).
    """

    BUY: int
    """Buy event."""

    SELL: int
    """Sell event."""

class LysTransport(Enum):
    """
    Lys transport mode enumeration.

    Represents the transaction broadcasting strategy.
    """

    STANDARD: int
    """Standard single broadcast to a single RPC."""

    NONCE: int
    """Nonce-based multi-broadcast for reliability (broadcasts to multiple RPCs)."""

    PRIORITY: int
    """Priority fee escalation for faster inclusion."""

class LysZmqClient:
    """
    ZeroMQ client for Lys Flash SDK transaction execution.

    This client communicates with the Lys Flash SDK via ZeroMQ protocol
    using MessagePack serialization for efficient binary data exchange.

    Parameters
    ----------
    endpoint : str
        The ZMQ endpoint (e.g., "ipc:///tmp/tx-executor.ipc" or "tcp://127.0.0.1:5555").
    timeout_secs : int, optional
        The timeout for operations in seconds (default: 30).

    """

    def __init__(
        self,
        endpoint: str,
        timeout_secs: int | None = None,
    ) -> None:
        """
        Initialize the ZMQ client.

        Parameters
        ----------
        endpoint : str
            The ZMQ endpoint.
        timeout_secs : int, optional
            The timeout in seconds.

        """
        ...

    async def execute_transaction(self, request_json: str) -> str:
        """
        Execute a Solana transaction via Lys Flash SDK.

        Parameters
        ----------
        request_json : str
            JSON string containing the transaction request with fields:
            - executionType: str (PUMP_FUN, RAYDIUM, JUPITER, CUSTOM)
            - eventType: str (BUY, SELL)
            - solAmountIn: int (amount in lamports)
            - tokenAmountOut: int
            - feePayer: str (Solana wallet address)
            - priorityFeeLamports: int
            - bribeLamports: int
            - transport: str (STANDARD, NONCE, PRIORITY)
            - tokenMint: str | None (Solana token mint address)

        Returns
        -------
        str
            JSON string containing the transaction response with fields:
            - success: bool
            - signature: str (Solana transaction signature)
            - error: str | None (error message if failed)

        Raises
        ------
        Exception
            If the transaction execution fails.

        """
        ...

    async def disconnect(self) -> None:
        """
        Disconnect the ZMQ client.

        Closes the ZeroMQ connection and cleans up resources.
        """
        ...

class LysWebSocketClient:
    """
    WebSocket client for Lys real-time Solana transaction monitoring.

    This client connects to the Lys WebSocket API to receive real-time
    notifications about Solana blockchain transactions and events.

    Parameters
    ----------
    base_url : str
        The WebSocket base URL (e.g., "wss://solana-mainnet-api-vip.lyslabs.ai/v1").
    api_key : str
        The Lys API key for authentication.

    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
    ) -> None:
        """
        Initialize the WebSocket client.

        Parameters
        ----------
        base_url : str
            The WebSocket base URL.
        api_key : str
            The Lys API key.

        """
        ...

    async def connect(self) -> Any:
        """
        Connect to the WebSocket server.

        Returns
        -------
        Any
            The WebSocket receiver stream for reading messages.

        Raises
        ------
        Exception
            If the connection fails.

        """
        ...

    async def disconnect(self) -> None:
        """
        Disconnect from the WebSocket server.

        Closes the WebSocket connection and cleans up resources.
        """
        ...

    async def subscribe_transactions(self) -> None:
        """
        Subscribe to transaction updates.

        Sends a subscription message to start receiving Solana transaction
        notifications through the WebSocket stream.

        Raises
        ------
        Exception
            If the subscription request fails.

        """
        ...

    async def unsubscribe_transactions(self) -> None:
        """
        Unsubscribe from transaction updates.

        Sends an unsubscription message to stop receiving transaction
        notifications.

        Raises
        ------
        Exception
            If the unsubscription request fails.

        """
        ...

    async def send_json(self, message: dict[str, Any]) -> None:
        """
        Send a JSON message to the WebSocket server.

        Parameters
        ----------
        message : dict[str, Any]
            The message to send.

        Raises
        ------
        Exception
            If sending the message fails.

        """
        ...

__all__ = [
    "LysExecutionType",
    "LysEventType",
    "LysTransport",
    "LysZmqClient",
    "LysWebSocketClient",
]
