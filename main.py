import importlib.metadata
import pathlib
import re
import sys


def _check_requirements():
    req = pathlib.Path(__file__).parent / "requirements.txt"
    if not req.exists():
        return
    missing = []
    for line in req.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[><=!~\[\s]", line)[0]
        try:
            importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            missing.append(line)
    if missing:
        print("Missing packages:")
        for p in missing:
            print(f"  {p}")
        print("\nInstall with: pip install -r requirements.txt")
        input("\nPress Enter to exit...")
        sys.exit(1)


_check_requirements()


import platform
import subprocess
import sys
import datetime
import warnings
from os import system
from time import sleep

# Ignore FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

system('clear' if platform.system() == 'nt' else 'cls')
print("Welcome to the Ethereum Transaction Tracker!\n\nBooting up...")


import requests
import yfinance as yf
import pandas as pd

""" Variables """

ETHERSCAN_API_KEY = 'YOUR_API_KEY'
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

""" Functions """

def get_transactions(wallet_address):
    """ Returns a list of transactions for the given address, including transaction fees. """
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    transactions = data['result']
    return transactions

def get_eth_price_at_date(date):
    """ Fetches the closing price of ETH on a specific date using Yahoo Finance. """
    eth = yf.Ticker("ETH-USD")
    hist = eth.history(start=date, end=date + datetime.timedelta(days=1))
    # Use .iloc[0] to access the first (and only) row's Close price safely
    return hist['Close'].iloc[0] if not hist.empty else 0


def get_eth_holdings(wallet_address):
    """Returns the current ETH holdings of the given address."""
    params = {
        'module': 'account',
        'action': 'balance',
        'address': wallet_address,
        'tag': 'latest',  # Fetches the latest balance
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    balance_wei = int(data['result'])
    balance_eth = balance_wei / 1e18  # Convert from wei to ETH
    return balance_eth


def analyze_transactions(transactions, wallet_address):
    """ Analyzes transactions to calculate detailed buy information and account for transaction fees. """
    buys = []
    total_spent_eth = 0
    total_fees_eth = 0

    for tx in transactions:
        if tx['to'].lower() == wallet_address:
            value_eth = int(tx['value']) / 1e18
            fee_eth = int(tx['gasUsed']) * int(tx['gasPrice']) / 1e18
            total_spent_eth += value_eth
            total_fees_eth += fee_eth
            timestamp = datetime.datetime.utcfromtimestamp(int(tx['timeStamp']))
            eth_price_usd = get_eth_price_at_date(timestamp.date())
            buys.append({'value_eth': value_eth, 'fee_eth': fee_eth, 'timestamp': timestamp, 'eth_price_usd': eth_price_usd})

    return buys, total_spent_eth, total_fees_eth

def calculate_profit_loss(buys, current_eth_price_usd):
    """ Calculates the unrealized profit or loss based on historical buys and current ETH price. """
    total_cost_usd = sum(buy['value_eth'] * buy['eth_price_usd'] for buy in buys)
    total_fees_usd = sum(buy['fee_eth'] * buy['eth_price_usd'] for buy in buys)
    total_acquisition_cost = total_cost_usd + total_fees_usd
    current_value_usd = current_eth_price_usd * sum(buy['value_eth'] for buy in buys)
    profit_loss_usd = current_value_usd - total_acquisition_cost
    profit_loss_percentage = (profit_loss_usd / total_acquisition_cost) * 100 if total_acquisition_cost else 0

    return profit_loss_usd, profit_loss_percentage

""" Main program """

if __name__ == '__main__':
    system('clear' if platform.system() == 'nt' else 'cls')
    print("Welcome to the Ethereum Transaction Tracker!\n")
    while True:
        try:
            wallet_address = input("Enter your Ethereum wallet address: ").lower()
            break
        except TypeError as e:
            system('clear' if platform.system() == 'nt' else 'cls')
            print("Welcome to the Ethereum Transaction Tracker!\n")
            print("Invalid wallet address. Please try again.")
            sleep(4)
            system('clear' if platform.system() == 'nt' else 'cls')
            print("Welcome to the Ethereum Transaction Tracker!\n")


    transactions = get_transactions(wallet_address)
    buys, total_spent_eth, total_fees_eth = analyze_transactions(transactions, wallet_address)
    current_eth_price_usd = get_eth_price_at_date(datetime.datetime.now().date())
    profit_loss_usd, profit_loss_percentage = calculate_profit_loss(buys, current_eth_price_usd)
    current_holdings_eth = get_eth_holdings(wallet_address)

    if profit_loss_usd >= 0:
        PROFIT_LOSS = 'Profit'
    else:
        PROFIT_LOSS = 'Loss'

    # After calculating your results, organize them into a DataFrame for neat output
    results_data = {
        "Category": ["Total ETH Holdings", "Total Fees in ETH", f"Currently In {PROFIT_LOSS}"],
        "ETH": [current_holdings_eth, total_fees_eth, "-"],
        "USD": [f"${total_spent_eth * current_eth_price_usd:.2f}", f"${total_fees_eth * current_eth_price_usd:.2f}", f"${profit_loss_usd:.2f}"],
        "Percentage": ["-", "-", f"{profit_loss_percentage:.2f}%"]
    }

    results_df = pd.DataFrame(results_data)

    # Optionally set the 'Category' column as the index for display purposes
    results_df.set_index("Category", inplace=True)

    print("\n", results_df)