# Eth-Transactions-Viewer

<p align="center">
  <img src="https://raw.githubusercontent.com/sayh3x/ETH-Transactions-Viewer/main/assets/main.webp" style="max-width: 100%; height: auto;" alt="Main logo">
</p>

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
    git clone https://github.com/sayh3x/eth-transactions-viewer.git
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

3. Save 

Enter `save` After enter wallet or ener `ctrl+c`

4. Delet Transactions File

 For Delet Enter `del` Or `rem` in Input Script

## Example



![Run](https://raw.githubusercontent.com/sayh3x/ETH-Transactions-Viewer/main/assets/work.gif)

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
```

## Troubleshooting

![Error](https://raw.githubusercontent.com/sayh3x/ETH-Transactions-Viewer/main/assets/error.gif)

If you encounter any errors while running the code, here are some potential problems and solutions:

### Problem: Network or Connectivity Issues
**Cause**: The code may fail to execute properly due to network connectivity issues.
**Solution**: Ensure that you have a stable internet connection. Check your network settings and try accessing other websites to verify your connection.

### Problem: API Endpoint Issues
**Cause**: The code may encounter errors if there is an issue with the API endpoint, such as Etherscan.io.
**Solution**: 
1. **Check the API Status**: Visit the [Etherscan.io status page](https://etherscan.io) to check if the API service is operational.
2. **Verify the API URL**: Ensure that the API endpoint URL in your code is correct.
3. **Inspect API Key**: If your API requires an API key, ensure that it is valid and has the necessary permissions.

### Problem: Wallet Address Issues
**Cause**: Errors can occur if the wallet address provided is incorrect or not formatted properly.
**Solution**: 
1. **Verify the Wallet Address**: Double-check the wallet address to ensure it is correct and follows the required format.
2. **Validate Address Format**: Ensure that the wallet address conforms to the expected format for the specific blockchain (e.g., Ethereum addresses should start with '0x').

### Example Check:
```sh
# Check internet connectivity
ping -c 4 google.com

# Check API endpoint status
curl -I https://api.etherscan.io/api

# Validate Ethereum wallet address format
if [[ $wallet_address =~ ^0x[a-fA-F0-9]{40}$ ]]; then
    echo "Valid wallet address"
else
    echo "Invalid wallet address"
fi
