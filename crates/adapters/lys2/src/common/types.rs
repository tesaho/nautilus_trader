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

//! Data types for the Lys adapter.

use serde::{Deserialize, Serialize};
use super::enums::{LysEventType, LysExecutionType, LysTransport};

/// Lys transaction request parameters
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LysTransactionRequest {
    /// Execution type (PUMP_FUN, RAYDIUM, etc.)
    pub execution_type: LysExecutionType,
    /// Event type (BUY or SELL)
    pub event_type: LysEventType,
    /// SOL amount in lamports
    pub sol_amount_in: u64,
    /// Minimum token amount out
    pub token_amount_out: u64,
    /// Fee payer public key
    pub fee_payer: String,
    /// Priority fee in lamports
    pub priority_fee_lamports: u64,
    /// Bribe amount in lamports (for validators)
    pub bribe_lamports: u64,
    /// Transport mechanism
    pub transport: LysTransport,
    /// Token mint address (for token operations)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub token_mint: Option<String>,
}

/// Lys transaction response
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LysTransactionResponse {
    /// Transaction signature
    pub signature: String,
    /// Success status
    pub success: bool,
    /// Error message (if failed)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}

/// Lys wallet information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LysWallet {
    /// Wallet public key
    pub public_key: String,
    /// Wallet label/name
    pub label: String,
}

/// Lys WebSocket subscription message
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LysWsSubscriptionMessage {
    /// Action type
    pub action: String,
}

/// Lys WebSocket transaction message
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LysWsTransactionMessage {
    /// Message type
    #[serde(rename = "type")]
    pub msg_type: String,
    /// Transaction signature
    pub signature: String,
    /// Transaction timestamp
    pub timestamp: i64,
    /// Additional data
    #[serde(flatten)]
    pub data: serde_json::Value,
}
