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
Example: Integrating Lys adapter with Nautilus Trader.

This example demonstrates how to set up and use the Lys adapter
for Solana trading with Nautilus Trader.
"""

import asyncio
import os
from decimal import Decimal

from nautilus_trader.adapters.lys2 import LYS
from nautilus_trader.adapters.lys2 import LysDataClientConfig
from nautilus_trader.adapters.lys2 import LysExecClientConfig
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.live.node import TradingNode


async def main():
    """
    Run the Lys adapter integration example.
    """
    print("Lys Adapter - Nautilus Trader Integration Example")
    print("=" * 50)
    print()

    # Get API key from environment
    api_key = os.getenv("LYS_API_KEY")
    if not api_key:
        print("Error: LYS_API_KEY environment variable not set")
        print("Please set it with: export LYS_API_KEY=your_api_key")
        return

    print(f"Using API Key: {api_key[:8]}...")
    print()

    # Configure data client (WebSocket for real-time monitoring)
    data_config = LysDataClientConfig(
        api_key=api_key,
        mainnet=True,  # Use Solana mainnet
        ws_base_url=None,  # Will use default mainnet URL
        timeout_secs=30,
    )

    # Configure execution client (ZMQ for transaction execution)
    exec_config = LysExecClientConfig(
        api_key=api_key,
        mainnet=True,  # Use Solana mainnet
        ws_base_url=None,  # Will use default mainnet URL
        zmq_endpoint=None,  # Will use default IPC endpoint
        use_zmq_ipc=True,  # Use IPC for better performance
        timeout_secs=30,
    )

    # Create trading node configuration
    config = TradingNodeConfig(
        trader_id=TraderId("TRADER-001"),
        data_clients={LYS: data_config},
        exec_clients={LYS: exec_config},
        # Add your strategy configurations here
    )

    print("Configuration created:")
    print(f"  - Data Client: {LYS}")
    print(f"  - Execution Client: {LYS}")
    print(f"  - Network: {'Mainnet' if data_config.mainnet else 'Devnet'}")
    print(f"  - ZMQ Transport: {'IPC' if exec_config.use_zmq_ipc else 'TCP'}")
    print()

    # Note: Actually creating and running the node requires a full Nautilus setup
    print("Note: To actually run the trading node:")
    print("1. Ensure the Lys Flash SDK is running at the ZMQ endpoint")
    print("2. Uncomment the node creation and execution code below")
    print("3. Add your trading strategies to the configuration")
    print()

    # Uncomment to actually create and run the node:
    # print("Creating trading node...")
    # node = TradingNode(config=config)
    #
    # print("Building trading node...")
    # node.build()
    #
    # print("Starting trading node...")
    # try:
    #     await node.run_async()
    # except KeyboardInterrupt:
    #     print("\nShutting down gracefully...")
    # finally:
    #     await node.stop_async()
    #     await node.dispose_async()

    print("Example configuration completed successfully!")
    print()
    print("Integration Points:")
    print("  1. WebSocket Data Client - Real-time Solana transaction monitoring")
    print("  2. ZMQ Execution Client - Transaction execution via Lys Flash SDK")
    print("  3. Instrument Provider - Dynamic Solana token instruments")
    print()
    print("Next Steps:")
    print("  - Implement your trading strategy")
    print("  - Configure risk management")
    print("  - Set up wallet addresses for transaction signing")
    print("  - Monitor positions and performance")


def example_direct_client_usage():
    """
    Example of using the Rust clients directly without Nautilus.
    """
    print("\nDirect Client Usage Example")
    print("=" * 50)
    print()

    try:
        from nautilus_lys2 import LysWebSocketClient, LysZmqClient

        print("1. Creating ZMQ Client:")
        zmq_client = LysZmqClient(
            endpoint="ipc:///tmp/tx-executor.ipc",
            timeout_secs=30,
        )
        print("   ✓ ZMQ client created")
        print()

        print("2. Creating WebSocket Client:")
        api_key = os.getenv("LYS_API_KEY", "your_api_key_here")
        ws_client = LysWebSocketClient(
            base_url="wss://solana-mainnet-api-vip.lyslabs.ai/v1",
            api_key=api_key,
        )
        print("   ✓ WebSocket client created")
        print()

        print("3. Usage:")
        print("   - Use zmq_client.execute_transaction() to submit transactions")
        print("   - Use ws_client.connect() to receive real-time updates")
        print()

    except ImportError as e:
        print(f"Error: Could not import Lys clients: {e}")
        print("Make sure the nautilus_lys2 extension is built and installed")


if __name__ == "__main__":
    # Run the main integration example
    asyncio.run(main())

    # Show direct client usage example
    example_direct_client_usage()
