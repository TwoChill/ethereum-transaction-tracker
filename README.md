# Ethereum Transaction Tracker

## Overview

The Ethereum Transaction Tracker is a Python script designed to fetch and visualize the transaction history and current balance of an Ethereum address. It leverages the Etherscan API to retrieve transaction data, which is then plotted to show the transaction values over time. This tool is invaluable for users looking to monitor transactions and balances of Ethereum wallets without needing direct access to them.

## Features

- **Balance Check**: Quickly fetch the current balance of any Ethereum address.
- **Transaction History**: Retrieve a comprehensive list of transactions for a given Ethereum address.
- **Data Visualization**: Plot the transaction history on a graph, showing the value of transactions in Ether.

## Prerequisites

Before using the Ethereum Transaction Tracker, ensure you have the following:

- Python 3.6 or newer.
- `requests` and `matplotlib` Python libraries installed.
- An Etherscan API Key.

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Usage

To use the Ethereum Transaction Tracker, follow these steps:

1. Execute the script in your terminal:

    ```bash
    python ethereum_transaction_tracker.py
    ```

2. When prompted, input the Ethereum address you want to track.

The script will display the current balance in Ether and a graph visualizing the address's transaction history.

## Contributing

Contributions are welcome! Feel free to fork this repository, make your improvements, and submit a pull request.

## License

This project is open source and available under the MIT License.
