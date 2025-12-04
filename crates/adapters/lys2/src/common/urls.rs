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

//! URL management for the Lys adapter.

use super::constants::{LYS_WS_MAINNET_URL, LYS_WS_DEVNET_URL, LYS_ZMQ_DEFAULT_IPC, LYS_ZMQ_DEFAULT_TCP};

/// Get WebSocket URL for the specified network
pub fn get_ws_url(mainnet: bool) -> &'static str {
    if mainnet {
        LYS_WS_MAINNET_URL
    } else {
        LYS_WS_DEVNET_URL
    }
}

/// Get ZMQ URL (IPC or TCP)
pub fn get_zmq_url(use_ipc: bool) -> &'static str {
    if use_ipc {
        LYS_ZMQ_DEFAULT_IPC
    } else {
        LYS_ZMQ_DEFAULT_TCP
    }
}

/// Build WebSocket URL with API key
pub fn build_ws_url_with_key(base_url: &str, api_key: &str) -> String {
    format!("{}/?apiKey={}", base_url, api_key)
}
