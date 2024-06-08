from dotenv import load_dotenv
from colorama import Fore
import pyfiglet as pyg
import time, os, requests, logging, webbrowser, sys

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set ETHERSCAN_API_KEY using environment variable or default value
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

VERSION = "1.0.1"
GITHUB_URL = "https://github.com/sayh3x/ETH-Transactions-Viewer"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def log_and_animate(message, duration=3, interval=0.5, level='INFO', mote='.'):
    log_message = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {level} - {message}'
    print(log_message, end='', flush=True)

    end_time = time.time() + duration
    while time.time() < end_time:
        for dots in range(4):
            sys.stdout.write(f'\r{log_message}{mote * dots}{" " * (3 - dots)}')
            sys.stdout.flush()
            time.sleep(interval)
    sys.stdout.write(f'\r{log_message}{mote * 3}\n')
    sys.stdout.flush()

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
            received_transactions = [{"value": tx["value"], "to": tx["to"], "tx_hash": tx["hash"], "from": tx["from"], "timestamp": tx["timeStamp"]} for tx in transactions if tx["to"].lower() == wallet_address.lower()]
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
    for tx in transactions:
        value_in_eth = int(tx["value"]) / 1e18
        usd_value = convert_to_usd(value_in_eth, eth_to_usd_rate)
        lower_sender_address = tx["from"]
        len_address = len(lower_sender_address)
        mid_point = len_address // 2

        balance = check_eth_balance(address=lower_sender_address, etherscan_api_key=ETHERSCAN_API_KEY)
        balance_in_usd = convert_to_usd(balance, eth_to_usd_rate)

        set_terminal_title(f"Sender Address: {lower_sender_address}")

        print()
        for i in range(len_address):
            if i == mid_point:
                print(f"'{lower_sender_address}'", end='')
            else:
                print('-', end='')
        print('\n')
        print(f"Send Value: {value_in_eth} ETH")
        print(f"ETH Balance: {balance}")
        print(f"Convert ETH to USD: {balance_in_usd}\n")

        print("-" * (len_address * 2))
        print()

def save_transactions(transactions, wallet_address, eth_to_usd_rate):
    log_and_animate(f'Save transactions in {wallet_address}.txt ', level='Saving', mote='#')
    if not os.path.exists('eth_log'):
        os.makedirs('eth_log')
                
    with open(os.path.join('eth_log', f'{wallet_address}.txt'), 'w') as file:
        for tx in transactions:
            value_in_eth = int(tx["value"]) / 1e18
            usd_value = convert_to_usd(value_in_eth, eth_to_usd_rate)
            file.write(f"Transaction Hash: {tx['tx_hash']}\n")
            file.write(f"Value: {value_in_eth} ETH\n")
            file.write(f"Value in USD: {usd_value}\n")
            file.write(f"From: {tx['from']}\n")
            file.write(f"To: {tx['to']}\n")
            file.write(f"Timestamp: {tx['timestamp']}\n")
            file.write("\n")

def check_wallet(text_input='Enter ERC-20 Wallet (enter 0 to visit GitHub): '):
    print(Fore.GREEN)
    try:
        wallet_address = input(text_input); print(Fore.RESET)
        
        if wallet_address == '0':
            clear()
            log_and_animate("Opening GitHub repository ", level='Waiting', mote='*')
            webbrowser.open(GITHUB_URL)
            check_wallet(text_input='Enter ERC-20 Wallet for exit(Entr 00): ')

        elif wallet_address == 'exit' or wallet_address == '00':
            clear()
            log_and_animate(Fore.YELLOW + "Bye ;", level='Exit', mote=')')
            sys.exit()

        log_and_animate('Checking wallet transactions')

        received_transactions = get_wallet_received_transactions(wallet_address, ETHERSCAN_API_KEY)
        if received_transactions:
            logging.info("Received Transactions:")
            eth_to_usd_rate = get_ethereum_price() or 0
            display_transactions(received_transactions, eth_to_usd_rate)

            save_transactions(received_transactions, wallet_address, eth_to_usd_rate)
        else:
            log_and_animate("No transactions found or 'Check Api Key'", level='Problem', mote='!')
    
    except KeyboardInterrupt:
        clear()
        print(Fore.RED + 'For exit Enter "exit" or "00".')
        time.sleep(1)
        log_and_animate('U KNOW ', level='Baby', mote='?')
        check_wallet()

def generate_logo():
    clear()
    logo = pyg.figlet_format('ETH Viewer', font='slant')
    print(Fore.CYAN + logo + Fore.RESET)
    print(Fore.RED + "𝘋𝘦𝘷𝘦𝘭𝘰𝘱𝘦𝘥 𝘣𝘺 𝙃3𝙓" + Fore.RESET)
    print(Fore.YELLOW + "Version: " + VERSION + Fore.RESET)

if __name__ == "__main__":
    generate_logo()
    check_wallet()
