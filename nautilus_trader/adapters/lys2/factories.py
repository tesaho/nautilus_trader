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
Factory functions for creating Lys adapter components.
"""

from functools import lru_cache

from nautilus_lys2 import LysWebSocketClient
from nautilus_lys2 import LysZmqClient

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import MessageBus
from nautilus_trader.live.factories import LiveDataClientFactory
from nautilus_trader.live.factories import LiveExecClientFactory

from nautilus_trader.adapters.lys2.config import LysDataClientConfig
from nautilus_trader.adapters.lys2.config import LysExecClientConfig
from nautilus_trader.adapters.lys2.constants import LYS_WS_DEVNET_URL
from nautilus_trader.adapters.lys2.constants import LYS_WS_MAINNET_URL
from nautilus_trader.adapters.lys2.constants import LYS_ZMQ_DEFAULT_IPC
from nautilus_trader.adapters.lys2.constants import LYS_ZMQ_DEFAULT_TCP
from nautilus_trader.adapters.lys2.data import LysDataClient
from nautilus_trader.adapters.lys2.execution import LysExecutionClient
from nautilus_trader.adapters.lys2.providers import LysInstrumentProvider


@lru_cache(maxsize=1)
def get_cached_lys_instrument_provider(
    mainnet: bool = True,
) -> LysInstrumentProvider:
    """
    Get a cached Lys instrument provider instance.

    Parameters
    ----------
    mainnet : bool, default True
        Whether to use mainnet (True) or devnet (False).

    Returns
    -------
    LysInstrumentProvider
        The cached instrument provider.

    """
    return LysInstrumentProvider(mainnet=mainnet)


@lru_cache(maxsize=1)
def get_cached_lys_ws_client(
    api_key: str,
    ws_base_url: str | None = None,
    mainnet: bool = True,
) -> LysWebSocketClient:
    """
    Get a cached Lys WebSocket client instance.

    Parameters
    ----------
    api_key : str
        The Lys API key for authentication.
    ws_base_url : str, optional
        The WebSocket base URL (default: mainnet or devnet based on mainnet flag).
    mainnet : bool, default True
        Whether to use mainnet (True) or devnet (False).

    Returns
    -------
    LysWebSocketClient
        The cached WebSocket client.

    """
    # Determine base URL
    if ws_base_url is None:
        ws_base_url = LYS_WS_MAINNET_URL if mainnet else LYS_WS_DEVNET_URL

    return LysWebSocketClient(base_url=ws_base_url, api_key=api_key)


@lru_cache(maxsize=1)
def get_cached_lys_zmq_client(
    zmq_endpoint: str | None = None,
    use_ipc: bool = True,
    timeout_secs: int = 30,
) -> LysZmqClient:
    """
    Get a cached Lys ZMQ client instance.

    Parameters
    ----------
    zmq_endpoint : str, optional
        The ZMQ endpoint for transaction execution.
        If None, uses default IPC or TCP endpoint based on use_ipc flag.
    use_ipc : bool, default True
        Whether to use IPC (True) or TCP (False) for ZMQ.
    timeout_secs : int, default 30
        The timeout for operations in seconds.

    Returns
    -------
    LysZmqClient
        The cached ZMQ client.

    """
    # Determine endpoint
    if zmq_endpoint is None:
        zmq_endpoint = LYS_ZMQ_DEFAULT_IPC if use_ipc else LYS_ZMQ_DEFAULT_TCP

    return LysZmqClient(endpoint=zmq_endpoint, timeout_secs=timeout_secs)


class LysLiveDataClientFactory(LiveDataClientFactory):
    """
    Factory for creating Lys live data clients.

    This factory creates LysDataClient instances with WebSocket connectivity
    for real-time Solana transaction monitoring.
    """

    @staticmethod
    def create(
        loop: object,
        name: str,
        config: LysDataClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
    ) -> LysDataClient:
        """
        Create a Lys live data client.

        Parameters
        ----------
        loop : object
            The event loop for the client.
        name : str
            The client name (not used, LYS_CLIENT_ID is used instead).
        config : LysDataClientConfig
            The client configuration.
        msgbus : MessageBus
            The message bus for the client.
        cache : Cache
            The cache for the client.
        clock : LiveClock
            The clock for the client.

        Returns
        -------
        LysDataClient
            The created data client.

        """
        # Get cached WebSocket client
        ws_client = get_cached_lys_ws_client(
            api_key=config.api_key,
            ws_base_url=config.ws_base_url,
            mainnet=config.mainnet,
        )

        # Create data client
        client = LysDataClient(
            loop=loop,
            client=ws_client,
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            config=config,
        )

        return client


class LysLiveExecClientFactory(LiveExecClientFactory):
    """
    Factory for creating Lys live execution clients.

    This factory creates LysExecutionClient instances with ZMQ connectivity
    for Solana transaction execution via Lys Flash SDK.
    """

    @staticmethod
    def create(
        loop: object,
        name: str,
        config: LysExecClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
    ) -> LysExecutionClient:
        """
        Create a Lys live execution client.

        Parameters
        ----------
        loop : object
            The event loop for the client.
        name : str
            The client name (not used, LYS_CLIENT_ID is used instead).
        config : LysExecClientConfig
            The client configuration.
        msgbus : MessageBus
            The message bus for the client.
        cache : Cache
            The cache for the client.
        clock : LiveClock
            The clock for the client.

        Returns
        -------
        LysExecutionClient
            The created execution client.

        """
        # Get cached ZMQ client
        zmq_client = get_cached_lys_zmq_client(
            zmq_endpoint=config.zmq_endpoint,
            use_ipc=config.use_zmq_ipc,
            timeout_secs=config.timeout_secs,
        )

        # Create execution client
        client = LysExecutionClient(
            loop=loop,
            client=zmq_client,
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            config=config,
        )

        return client
