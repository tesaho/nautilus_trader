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
Configuration for the Lys adapter.
"""

from nautilus_trader.config import LiveDataClientConfig
from nautilus_trader.config import LiveExecClientConfig


class LysDataClientConfig(LiveDataClientConfig, frozen=True):
    """
    Configuration for `LysDataClient` instances.

    Parameters
    ----------
    api_key : str
        The Lys API key for authentication.
    ws_base_url : str, optional
        The WebSocket base URL (default: mainnet).
    mainnet : bool, default True
        Whether to use mainnet (True) or devnet (False).
    timeout_secs : int, default 30
        The timeout for operations in seconds.
    """

    api_key: str
    ws_base_url: str | None = None
    mainnet: bool = True
    timeout_secs: int = 30


class LysExecClientConfig(LiveExecClientConfig, frozen=True):
    """
    Configuration for `LysExecutionClient` instances.

    Parameters
    ----------
    api_key : str
        The Lys API key for authentication.
    ws_base_url : str, optional
        The WebSocket base URL (default: mainnet).
    zmq_endpoint : str, optional
        The ZMQ endpoint for transaction execution.
    mainnet : bool, default True
        Whether to use mainnet (True) or devnet (False).
    use_zmq_ipc : bool, default True
        Whether to use IPC (True) or TCP (False) for ZMQ.
    timeout_secs : int, default 30
        The timeout for operations in seconds.
    """

    api_key: str
    ws_base_url: str | None = None
    zmq_endpoint: str | None = None
    mainnet: bool = True
    use_zmq_ipc: bool = True
    timeout_secs: int = 30
