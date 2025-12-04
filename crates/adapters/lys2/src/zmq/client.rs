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

//! ZMQ client implementation for Lys Flash SDK.

use std::time::Duration;
use rmp_serde::{Deserializer, Serializer};
use serde::{Deserialize, Serialize};
use tmq::{request, Context};
use tracing::{debug, error, info};

use crate::common::{
    constants::LYS_DEFAULT_TIMEOUT,
    errors::LysZmqError,
    types::{LysTransactionRequest, LysTransactionResponse},
};

/// Lys ZMQ client for executing transactions via Lys Flash SDK
#[derive(Clone)]
pub struct LysZmqClient {
    endpoint: String,
    timeout: Duration,
    context: Context,
}

impl LysZmqClient {
    /// Create a new Lys ZMQ client
    ///
    /// # Arguments
    /// * `endpoint` - ZMQ endpoint (e.g., "ipc:///tmp/tx-executor.ipc" or "tcp://127.0.0.1:5555")
    /// * `timeout_secs` - Operation timeout in seconds
    pub fn new(endpoint: String, timeout_secs: Option<u64>) -> Self {
        let timeout = Duration::from_secs(timeout_secs.unwrap_or(LYS_DEFAULT_TIMEOUT));
        let context = Context::new();

        info!("Creating Lys ZMQ client with endpoint: {}", endpoint);

        Self {
            endpoint,
            timeout,
            context,
        }
    }

    /// Execute a transaction via Lys Flash SDK
    ///
    /// # Arguments
    /// * `request` - Transaction request parameters
    ///
    /// # Returns
    /// * `Result<LysTransactionResponse, LysZmqError>` - Transaction response or error
    pub async fn execute_transaction(
        &self,
        request: &LysTransactionRequest,
    ) -> Result<LysTransactionResponse, LysZmqError> {
        debug!("Executing transaction: {:?}", request);

        // Serialize request to MessagePack
        let mut buf = Vec::new();
        request
            .serialize(&mut Serializer::new(&mut buf))
            .map_err(|e| LysZmqError::SerializationError(e.to_string()))?;

        // Create REQ socket
        let mut socket = request(&self.context)
            .connect(&self.endpoint)
            .map_err(|e| LysZmqError::ConnectionError(e.to_string()))?;

        // Send request
        socket
            .send(buf)
            .await
            .map_err(|e| LysZmqError::SendError(e.to_string()))?;

        // Receive response with timeout
        let response_bytes = tokio::time::timeout(self.timeout, socket.recv())
            .await
            .map_err(|_| LysZmqError::Timeout(self.timeout.as_secs()))?
            .map_err(|e| LysZmqError::ReceiveError(e.to_string()))?;

        // Deserialize response from MessagePack
        let mut de = Deserializer::new(&response_bytes[..]);
        let response: LysTransactionResponse = Deserialize::deserialize(&mut de)
            .map_err(|e| LysZmqError::DeserializationError(e.to_string()))?;

        if response.success {
            info!("Transaction executed successfully: {}", response.signature);
        } else {
            error!(
                "Transaction failed: {}",
                response.error.as_deref().unwrap_or("Unknown error")
            );
        }

        Ok(response)
    }

    /// Get the configured endpoint
    pub fn endpoint(&self) -> &str {
        &self.endpoint
    }

    /// Get the configured timeout
    pub fn timeout(&self) -> Duration {
        self.timeout
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::enums::{LysEventType, LysExecutionType, LysTransport};

    #[test]
    fn test_zmq_client_creation() {
        let client = LysZmqClient::new("ipc:///tmp/test.ipc".to_string(), Some(10));
        assert_eq!(client.endpoint(), "ipc:///tmp/test.ipc");
        assert_eq!(client.timeout(), Duration::from_secs(10));
    }

    #[test]
    fn test_transaction_request_serialization() {
        let request = LysTransactionRequest {
            execution_type: LysExecutionType::PumpFun,
            event_type: LysEventType::Buy,
            sol_amount_in: 1_000_000_000, // 1 SOL
            token_amount_out: 1000,
            fee_payer: "test_pubkey".to_string(),
            priority_fee_lamports: 5000,
            bribe_lamports: 1000,
            transport: LysTransport::Nonce,
            token_mint: Some("token_mint_address".to_string()),
        };

        let mut buf = Vec::new();
        request.serialize(&mut Serializer::new(&mut buf)).unwrap();
        assert!(!buf.is_empty());
    }
}
