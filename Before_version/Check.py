import logging, requests, time, os

Addres_Wallet= str(input('Enter Wallet : '))
eth_scan_apikey = '' # Youre API Key


def check_ETH_balance(address, etherscan_api_key, retries=3, delay=5):
    # Etherscan API endpoint to check the balance of an address
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"

    for attempt in range(retries):
        try:
            # Make a request to the Etherscan API
            response = requests.get(api_url)
            data = response.json()

            # Check if the request was successful
            if data["status"] == "1":
                # Convert Wei to Ether (1 Ether = 10^18 Wei)
                balance = int(data["result"]) / 1e18
                return balance
            else:
                logging.error("Error getting balance: %s", data["message"])
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(
                    f"Error checking balance, retrying in {delay} seconds: {str(e)}"
                )
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
            print("Error:", data["message"])
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def calculate_length(text):
    length = len(text)
    return length


def get_ethereum_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        data = response.json()
        
        ethereum_price = data["ethereum"]["usd"]
        
        return ethereum_price
    except Exception as e:
        print("Limit Requests :", str(e))
        return None

def convert_to_usd(eth_amount, eth_to_usd_rate):
    return eth_amount * eth_to_usd_rate


# def check_wallet():
#     received_transactions = get_wallet_received_transactions(Addres_Wallet, eth_scan_apikey)
#     len_addres = calculate_length(text=receiver_address)
#     mid_point = len_addres// 2 

#     balance = check_ETH_balance(address=receiver_address, etherscan_api_key=eth_scan_apikey)

#     eth_balance = balance
#     eth_to_usd_rate = get_ethereum_price()

#     balance_in_usd = convert_to_usd(eth_balance, eth_to_usd_rate)

#     globals
#     if received_transactions:

#         print("Received Transactions:")
#         for value, receiver_address in received_transactions:
#             print("Transaction Value:", value)
#             print("Receiver Address:", receiver_address)
#             print()

    # for check in range(receiver_address):
    #     print()
    #     for i in range(len_addres):
    #         if i == mid_point:
    #             print(f"'{check}'.Check Wallet", end='')
    #         else:
    #             print('-', end='')
    #     print('\n')
    #     print(f"Addres ETH : ", receiver_address)
    #     print(f"ETH Balance : ", balance)
    #     print(f"Convert ETH to USDT :" ,balance_in_usd, '\n')

    #     for i in range(len_addres+11):
    #         print("-", end="")


def set_terminal_title(title):
    os.system(f"echo -n \"\\033]0;{title}\\007\"")

def check_wallet():

    print("Checking wallet transactions...")

    received_transactions = get_wallet_received_transactions(Addres_Wallet, eth_scan_apikey)
    number_of_addresses = len(received_transactions)
    if received_transactions:
        print("Received Transactions:")
        for value, receiver_address in received_transactions:
            print("Transaction Value:", value)
            print("Receiver Address:", receiver_address)
            print()

    for value, sender_address in received_transactions:
        lower_sender_address = sender_address 
        len_addres = calculate_length(text=lower_sender_address)
        mid_point = len_addres // 2 
        balance = check_ETH_balance(address=lower_sender_address, etherscan_api_key=eth_scan_apikey)
        eth_balance = balance
        eth_to_usd_rate = 3204
        balance_in_usd = convert_to_usd(eth_balance, eth_to_usd_rate)

        set_terminal_title(f"Sender Address: {lower_sender_address}")

        print()
        for i in range(len_addres):
            if i == mid_point:
                print(f"'{lower_sender_address}'", end='')
            else:
                print('-', end='')
        print('\n')
        # print(f"Addres ETH : ", lower_sender_address)
        print(f"send Value : ", value)
        print(f"ETH Balance : ", balance)
        print(f"Convert ETH to USDT :" ,balance_in_usd, '\n')

        for i in range(len_addres*2):
            print("-", end="")
        print()


check_wallet()
