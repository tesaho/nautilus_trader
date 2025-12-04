// -------------------------------------------------------------------------------------------------
//  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
//  https://nautechsystems.io
//
//  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
//  You may not use this file except in compliance with the License.
//  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
// -------------------------------------------------------------------------------------------------

//! Constants for the Lys adapter.

// WebSocket URLs
pub const LYS_WS_MAINNET_URL: &str = "wss://solana-mainnet-api-vip.lyslabs.ai/v1";
pub const LYS_WS_DEVNET_URL: &str = "wss://solana-devnet-api.lyslabs.ai/v1";

// ZMQ URLs
pub const LYS_ZMQ_DEFAULT_IPC: &str = "ipc:///tmp/tx-executor.ipc";
pub const LYS_ZMQ_DEFAULT_TCP: &str = "tcp://127.0.0.1:5555";

// Default timeouts (in seconds)
pub const LYS_DEFAULT_TIMEOUT: u64 = 30;
pub const LYS_WS_HEARTBEAT: u64 = 60;

// Lamports conversion
pub const LAMPORTS_PER_SOL: u64 = 1_000_000_000;

// Venue identifier
pub const LYS_VENUE: &str = "LYS";
