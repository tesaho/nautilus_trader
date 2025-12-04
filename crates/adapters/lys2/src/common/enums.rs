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

//! Enums for the Lys adapter.

use serde::{Deserialize, Serialize};

/// Lys execution type (operation type)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum LysExecutionType {
    /// Pump.fun token operations
    PumpFun,
    /// Raydium DEX operations
    Raydium,
    /// Jupiter aggregator operations
    Jupiter,
    /// Generic Solana program interaction
    Custom,
}

/// Lys event type (buy or sell action)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum LysEventType {
    /// Buy tokens
    Buy,
    /// Sell tokens
    Sell,
}

/// Lys transport mechanism for transaction broadcasting
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum LysTransport {
    /// Standard single broadcast
    Standard,
    /// Nonce-based multi-broadcast for reliability
    Nonce,
    /// Priority fee escalation
    Priority,
}

/// Lys WebSocket message type
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LysWsMessageType {
    /// Subscription confirmation
    Subscription,
    /// Single transaction event
    Transaction,
    /// Multiple transaction events
    Transactions,
    /// Server information
    Info,
    /// Server error
    Error,
}

/// Lys WebSocket action type
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LysWsAction {
    /// Subscribe to transaction stream
    Subscribe,
    /// Unsubscribe from transaction stream
    Unsubscribe,
}

impl std::fmt::Display for LysExecutionType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::PumpFun => write!(f, "PUMP_FUN"),
            Self::Raydium => write!(f, "RAYDIUM"),
            Self::Jupiter => write!(f, "JUPITER"),
            Self::Custom => write!(f, "CUSTOM"),
        }
    }
}

impl std::fmt::Display for LysEventType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Buy => write!(f, "BUY"),
            Self::Sell => write!(f, "SELL"),
        }
    }
}

impl std::fmt::Display for LysTransport {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Standard => write!(f, "STANDARD"),
            Self::Nonce => write!(f, "NONCE"),
            Self::Priority => write!(f, "PRIORITY"),
        }
    }
}
