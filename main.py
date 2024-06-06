import logging
import requests
import time
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set ETHERSCAN_API_KEY using environment variable or default value
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

def check_eth_balance(address, etherscan_api_key, retries=3, delay=5):
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"

    for attempt in range(retries):
        try:
            response = requests.get(api_url)
            data = response.json()

            if data["status"] == "1":
                balance = int(data["result"]) / 1e18
                return balance
            else:
                logging.error("Error getting balance: %s", data["message"])
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0

def get_wallet_received_transactions(wallet_address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "1":
            transactions = data["result"]
            received_transactions = [(tx["value"], tx["to"]) for tx in transactions if tx["to"].lower() != wallet_address.lower()]
            return received_transactions
        else:
            logging.error("Error: %s", data["message"])
            return None
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return None

def get_ethereum_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        data = response.json()
        ethereum_price = data["ethereum"]["usd"]
        return ethereum_price
    except Exception as e:
        logging.error("Error fetching Ethereum price: %s", str(e))
        return None

def convert_to_usd(eth_amount, eth_to_usd_rate):
    return eth_amount * eth_to_usd_rate

def set_terminal_title(title):
    os.system(f"echo -n \"\\033]0;{title}\\007\"")

def display_transactions(transactions, eth_to_usd_rate):
    for value, sender_address in transactions:
        lower_sender_address = sender_address 
        len_addres = len(lower_sender_address)
        mid_point = len_addres // 2 

        balance = check_eth_balance(address=lower_sender_address, etherscan_api_key=ETHERSCAN_API_KEY)
        balance_in_usd = convert_to_usd(balance, eth_to_usd_rate)

        set_terminal_title(f"Sender Address: {lower_sender_address}")

        print()
        for i in range(len_addres):
            if i == mid_point:
                print(f"'{lower_sender_address}'", end='')
            else:
                print('-', end='')
        print('\n')
        print(f"Send Value: {value}")
        print(f"ETH Balance: {balance}")
        print(f"Convert ETH to USD: {balance_in_usd}\n")

        print("-" * (len_addres * 2))
        print()

def check_wallet():
    wallet_address = input('Enter ERC-20 Wallet : ')
    logging.info("Checking wallet transactions...")

    received_transactions = get_wallet_received_transactions(wallet_address, ETHERSCAN_API_KEY)
    if received_transactions:
        logging.info("Received Transactions:")
        eth_to_usd_rate = get_ethereum_price() or 0
        display_transactions(received_transactions, eth_to_usd_rate)
    else:
        logging.info("No transactions found or an error occurred.")

if __name__ == "__main__":
    check_wallet()
