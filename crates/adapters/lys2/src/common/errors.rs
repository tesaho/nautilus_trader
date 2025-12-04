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

//! Error types for the Lys adapter.

use thiserror::Error;

/// Errors that can occur when using the Lys ZMQ client
#[derive(Error, Debug)]
pub enum LysZmqError {
    /// ZMQ connection error
    #[error("ZMQ connection error: {0}")]
    ConnectionError(String),

    /// ZMQ send error
    #[error("ZMQ send error: {0}")]
    SendError(String),

    /// ZMQ receive error
    #[error("ZMQ receive error: {0}")]
    ReceiveError(String),

    /// MessagePack serialization error
    #[error("MessagePack serialization error: {0}")]
    SerializationError(String),

    /// MessagePack deserialization error
    #[error("MessagePack deserialization error: {0}")]
    DeserializationError(String),

    /// Timeout error
    #[error("Operation timed out after {0} seconds")]
    Timeout(u64),

    /// Invalid response
    #[error("Invalid response: {0}")]
    InvalidResponse(String),
}

/// Errors that can occur when using the Lys WebSocket client
#[derive(Error, Debug)]
pub enum LysWsError {
    /// WebSocket connection error
    #[error("WebSocket connection error: {0}")]
    ConnectionError(String),

    /// WebSocket send error
    #[error("WebSocket send error: {0}")]
    SendError(String),

    /// WebSocket receive error
    #[error("WebSocket receive error: {0}")]
    ReceiveError(String),

    /// JSON parsing error
    #[error("JSON parsing error: {0}")]
    JsonError(#[from] serde_json::Error),

    /// Authentication error
    #[error("Authentication failed: {0}")]
    AuthenticationError(String),

    /// Subscription error
    #[error("Subscription error: {0}")]
    SubscriptionError(String),

    /// Invalid message format
    #[error("Invalid message format: {0}")]
    InvalidMessage(String),
}

/// Errors that can occur when using the Lys HTTP client
#[derive(Error, Debug)]
pub enum LysHttpError {
    /// HTTP request error
    #[error("HTTP request error: {0}")]
    RequestError(#[from] reqwest::Error),

    /// Invalid API key
    #[error("Invalid API key")]
    InvalidApiKey,

    /// Rate limit exceeded
    #[error("Rate limit exceeded")]
    RateLimitExceeded,

    /// Invalid response
    #[error("Invalid response: {0}")]
    InvalidResponse(String),
}
