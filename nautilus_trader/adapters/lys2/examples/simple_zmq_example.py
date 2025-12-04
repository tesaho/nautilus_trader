#!/usr/bin/env python3
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
Example: Simple ZMQ client usage for transaction execution.

This example demonstrates how to use the LysZmqClient directly
to execute Solana transactions via the Lys Flash SDK.
"""

import asyncio
import json

from nautilus_lys2 import LysZmqClient


async def main():
    """
    Run a simple transaction execution example.
    """
    print("Simple Lys ZMQ Client Example")
    print("=" * 50)
    print()

    # Create ZMQ client
    client = LysZmqClient(
        endpoint="ipc:///tmp/tx-executor.ipc",
        timeout_secs=30,
    )

    print("Created ZMQ client")
    print("Endpoint: ipc:///tmp/tx-executor.ipc")
    print("Timeout: 30 seconds")
    print()

    # Create a transaction request
    request = {
        "executionType": "PUMP_FUN",
        "eventType": "BUY",
        "solAmountIn": 1_000_000_000,  # 1 SOL in lamports
        "tokenAmountOut": 1000,
        "feePayer": "YourWalletPublicKeyHere",
        "priorityFeeLamports": 5000,
        "bribeLamports": 1000,
        "transport": "NONCE",  # Multi-broadcast for reliability
        "tokenMint": "TokenMintAddressHere",
    }

    print("Transaction Request:")
    print(json.dumps(request, indent=2))
    print()

    print("Note: This will fail unless the Lys Flash SDK is running.")
    print("To actually execute transactions:")
    print("  1. Start the Lys Flash SDK at the ZMQ endpoint")
    print("  2. Replace 'YourWalletPublicKeyHere' with your actual wallet")
    print("  3. Replace 'TokenMintAddressHere' with the target token mint")
    print("  4. Uncomment the execution code below")
    print()

    # Uncomment to actually execute:
    # try:
    #     print("Executing transaction...")
    #     response_json = await client.execute_transaction(json.dumps(request))
    #     response = json.loads(response_json)
    #
    #     print("\nTransaction Response:")
    #     print(json.dumps(response, indent=2))
    #
    #     if response.get("success"):
    #         print("\n✓ Transaction successful!")
    #         print(f"  Signature: {response.get('signature')}")
    #     else:
    #         print("\n✗ Transaction failed!")
    #         print(f"  Error: {response.get('error')}")
    #
    # except Exception as e:
    #     print(f"\n✗ Error executing transaction: {e}")

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
