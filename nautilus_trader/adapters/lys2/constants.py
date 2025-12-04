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
Constants for the Lys adapter.
"""

from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import Venue


LYS = "LYS"
LYS_VENUE = Venue(LYS)
LYS_CLIENT_ID = ClientId(LYS)

# WebSocket URLs
LYS_WS_MAINNET_URL = "wss://solana-mainnet-api-vip.lyslabs.ai/v1"
LYS_WS_DEVNET_URL = "wss://solana-devnet-api.lyslabs.ai/v1"

# ZMQ URLs
LYS_ZMQ_DEFAULT_IPC = "ipc:///tmp/tx-executor.ipc"
LYS_ZMQ_DEFAULT_TCP = "tcp://127.0.0.1:5555"

# Timeouts
LYS_DEFAULT_TIMEOUT = 30

# Solana constants
LAMPORTS_PER_SOL = 1_000_000_000
