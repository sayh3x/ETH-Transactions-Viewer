# Eth-Transactions-Viewer

Eth-Transactions-Viewer is a Python script designed to check the balance of an Ethereum wallet and retrieve transaction information. This tool interacts with the Etherscan API to provide detailed insights into wallet activity and balance.

## Features

- Check Ethereum wallet balance.
- Retrieve and display wallet transactions.
- Convert ETH balance to USD using real-time exchange rates from CoinGecko.
- Log and handle errors gracefully.
- Set terminal title to reflect current operations.

## Requirements

- Python 3.x
- `requests` library
- Etherscan API key

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/eth-transactions-viewer.git
    cd eth-transactions-viewer
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Etherscan API key:

    - Create a `.env` file in the root directory of the project.
    - Add your Etherscan API key to the `.env` file:

      ```env
      ETHERSCAN_API_KEY=your_etherscan_api_key_here
      ```

## Usage

1. Run the script:

    ```bash
    python eth_transactions_viewer.py
    ```

2. Enter the Ethereum wallet address when prompted.

The script will output the received transactions, wallet balance, and the balance converted to USD.

## Example

```bash
$ python eth_transactions_viewer.py
Enter ERC-20 Wallet : 0x3D55CCb2a943d88D39dd2E62DAf767C69fD0179F
2024-06-06 06:38:46,169 - INFO - Checking wallet transactions...
2024-06-06 06:38:53,121 - INFO - Received Transactions:

---------------------'0xdac17f958d2ee523a2206206994597c13d831ec7'--------------------

Send Value: 0
ETH Balance: 1e-18
Convert ETH to USD: 3.847840000000001e-15

------------------------------------------------------------------------------------


---------------------'0xdac17f958d2ee523a2206206994597c13d831ec7'--------------------

Send Value: 0
ETH Balance: 1e-18
Convert ETH to USD: 3.847840000000001e-15

------------------------------------------------------------------------------------
