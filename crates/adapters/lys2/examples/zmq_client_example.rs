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

//! Example: Using the Lys ZMQ client for transaction execution.
//!
//! This example demonstrates how to use the LysZmqClient to execute
//! Solana transactions via the Lys Flash SDK.

use nautilus_lys2::{
    common::{
        enums::{LysEventType, LysExecutionType, LysTransport},
        types::LysTransactionRequest,
    },
    zmq::LysZmqClient,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Lys ZMQ Client Example");
    println!("======================\n");

    // Create ZMQ client
    // In production, this would connect to the Lys Flash SDK endpoint
    let client = LysZmqClient::new("ipc:///tmp/tx-executor.ipc".to_string(), Some(30));

    println!("Created ZMQ client connected to: ipc:///tmp/tx-executor.ipc\n");

    // Create a transaction request
    let request = LysTransactionRequest {
        execution_type: LysExecutionType::PumpFun,
        event_type: LysEventType::Buy,
        sol_amount_in: 1_000_000_000, // 1 SOL
        token_amount_out: 1000,
        fee_payer: "YourWalletAddressHere".to_string(),
        priority_fee_lamports: 5000,
        bribe_lamports: 1000,
        transport: LysTransport::Nonce, // Multi-broadcast for reliability
        token_mint: Some("TokenMintAddressHere".to_string()),
    };

    println!("Transaction Request:");
    println!("  Execution Type: {:?}", request.execution_type);
    println!("  Event Type: {:?}", request.event_type);
    println!("  SOL Amount: {} lamports (1 SOL)", request.sol_amount_in);
    println!("  Token Amount Out: {}", request.token_amount_out);
    println!("  Priority Fee: {} lamports", request.priority_fee_lamports);
    println!("  Bribe: {} lamports", request.bribe_lamports);
    println!("  Transport: {:?}", request.transport);
    println!();

    // Note: This will fail if the Lys Flash SDK is not running
    println!("Note: Make sure the Lys Flash SDK is running at the ZMQ endpoint");
    println!("before executing transactions.\n");

    // Uncomment to actually execute (requires running Lys Flash SDK):
    // match client.execute_transaction(&request).await {
    //     Ok(response) => {
    //         println!("Transaction Success!");
    //         println!("  Signature: {}", response.signature);
    //         if let Some(slot) = response.slot {
    //             println!("  Slot: {}", slot);
    //         }
    //     }
    //     Err(e) => {
    //         eprintln!("Transaction Failed: {}", e);
    //     }
    // }

    println!("Example completed successfully!");

    Ok(())
}
