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

//! WebSocket client implementation for Lys real-time data.

use std::sync::Arc;
use futures::stream::{SplitSink, SplitStream};
use futures::{SinkExt, StreamExt};
use serde_json::json;
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio_tungstenite::{connect_async, MaybeTlsStream, WebSocketStream};
use tokio_tungstenite::tungstenite::Message;
use tracing::{debug, error, info, warn};

use crate::common::{
    errors::LysWsError,
    types::LysWsSubscriptionMessage,
    urls::build_ws_url_with_key,
};

type WsStream = WebSocketStream<MaybeTlsStream<TcpStream>>;
type WsSink = SplitSink<WsStream, Message>;
type WsReceiver = SplitStream<WsStream>;

/// Lys WebSocket client for real-time transaction monitoring
#[derive(Clone)]
pub struct LysWebSocketClient {
    inner: Arc<Inner>,
}

struct Inner {
    base_url: String,
    api_key: String,
    sink: Arc<Mutex<Option<WsSink>>>,
    is_connected: Arc<Mutex<bool>>,
}

impl LysWebSocketClient {
    /// Create a new Lys WebSocket client
    ///
    /// # Arguments
    /// * `base_url` - WebSocket base URL
    /// * `api_key` - Lys API key
    pub fn new(base_url: String, api_key: String) -> Self {
        info!("Creating Lys WebSocket client");

        Self {
            inner: Arc::new(Inner {
                base_url,
                api_key,
                sink: Arc::new(Mutex::new(None)),
                is_connected: Arc::new(Mutex::new(false)),
            }),
        }
    }

    /// Connect to the WebSocket server
    pub async fn connect(&self) -> Result<WsReceiver, LysWsError> {
        let url = build_ws_url_with_key(&self.inner.base_url, &self.inner.api_key);
        info!("Connecting to Lys WebSocket: {}", self.inner.base_url);

        let (ws_stream, _) = connect_async(&url)
            .await
            .map_err(|e| LysWsError::ConnectionError(e.to_string()))?;

        let (sink, stream) = ws_stream.split();

        *self.inner.sink.lock().await = Some(sink);
        *self.inner.is_connected.lock().await = true;

        info!("Successfully connected to Lys WebSocket");
        Ok(stream)
    }

    /// Subscribe to transaction stream
    pub async fn subscribe_transactions(&self) -> Result<(), LysWsError> {
        if !*self.inner.is_connected.lock().await {
            return Err(LysWsError::ConnectionError(
                "Not connected. Call connect() first".to_string(),
            ));
        }

        let subscription_msg = json!({
            "action": "subscribe"
        });

        self.send_json(&subscription_msg).await?;
        info!("Subscribed to Lys transaction stream");
        Ok(())
    }

    /// Unsubscribe from transaction stream
    pub async fn unsubscribe_transactions(&self) -> Result<(), LysWsError> {
        if !*self.inner.is_connected.lock().await {
            return Err(LysWsError::ConnectionError("Not connected".to_string()));
        }

        let unsubscription_msg = json!({
            "action": "unsubscribe"
        });

        self.send_json(&unsubscription_msg).await?;
        info!("Unsubscribed from Lys transaction stream");
        Ok(())
    }

    /// Send a JSON message to the WebSocket
    async fn send_json(&self, msg: &serde_json::Value) -> Result<(), LysWsError> {
        let mut sink_guard = self.inner.sink.lock().await;

        if let Some(sink) = sink_guard.as_mut() {
            let text = serde_json::to_string(msg)?;
            sink.send(Message::Text(text))
                .await
                .map_err(|e| LysWsError::SendError(e.to_string()))?;
            debug!("Sent message: {}", msg);
            Ok(())
        } else {
            Err(LysWsError::ConnectionError("No active connection".to_string()))
        }
    }

    /// Check if connected
    pub async fn is_connected(&self) -> bool {
        *self.inner.is_connected.lock().await
    }

    /// Disconnect from WebSocket
    pub async fn disconnect(&self) -> Result<(), LysWsError> {
        info!("Disconnecting from Lys WebSocket");

        let mut sink_guard = self.inner.sink.lock().await;
        if let Some(mut sink) = sink_guard.take() {
            sink.close()
                .await
                .map_err(|e| LysWsError::ConnectionError(e.to_string()))?;
        }

        *self.inner.is_connected.lock().await = false;
        info!("Disconnected from Lys WebSocket");
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ws_client_creation() {
        let client = LysWebSocketClient::new(
            "wss://test.example.com".to_string(),
            "test_api_key".to_string(),
        );

        // Basic creation test
        assert!(client.inner.base_url.contains("test.example.com"));
    }

    #[tokio::test]
    async fn test_ws_client_not_connected() {
        let client = LysWebSocketClient::new(
            "wss://test.example.com".to_string(),
            "test_api_key".to_string(),
        );

        assert!(!client.is_connected().await);
    }
}
