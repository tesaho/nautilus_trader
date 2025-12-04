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

//! Example: Using the Lys WebSocket client for real-time monitoring.
//!
//! This example demonstrates how to use the LysWebSocketClient to monitor
//! Solana transactions in real-time.

use futures_util::StreamExt;
use nautilus_lys2::websocket::LysWebSocketClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Lys WebSocket Client Example");
    println!("============================\n");

    // Create WebSocket client
    // Replace with your actual API key
    let api_key = std::env::var("LYS_API_KEY").unwrap_or_else(|_| "your_api_key_here".to_string());

    let client = LysWebSocketClient::new(
        "wss://solana-mainnet-api-vip.lyslabs.ai/v1".to_string(),
        api_key.clone(),
    );

    println!("Created WebSocket client");
    println!("Base URL: wss://solana-mainnet-api-vip.lyslabs.ai/v1");
    println!("API Key: {}...\n", &api_key[..8.min(api_key.len())]);

    // Note: This will fail if you don't have a valid API key
    println!("Note: Set the LYS_API_KEY environment variable with your API key");
    println!("to actually connect to the WebSocket server.\n");

    // Uncomment to actually connect and receive messages:
    // println!("Connecting to WebSocket...");
    // let mut stream = client.connect().await?;
    // println!("Connected successfully!\n");

    // println!("Subscribing to transactions...");
    // client.subscribe_transactions().await?;
    // println!("Subscribed!\n");

    // println!("Receiving messages (press Ctrl+C to stop)...\n");
    // while let Some(message) = stream.next().await {
    //     match message {
    //         Ok(msg) => {
    //             if let Ok(text) = msg.to_text() {
    //                 println!("Received: {}", text);
    //             }
    //         }
    //         Err(e) => {
    //             eprintln!("Error receiving message: {}", e);
    //             break;
    //         }
    //     }
    // }

    // println!("\nDisconnecting...");
    // client.disconnect().await?;
    // println!("Disconnected successfully!");

    println!("Example completed successfully!");
    println!("\nTo run this example with actual WebSocket connection:");
    println!("  export LYS_API_KEY=your_actual_api_key");
    println!("  cargo run --example websocket_client_example");

    Ok(())
}
