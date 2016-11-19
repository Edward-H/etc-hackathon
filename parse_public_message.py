# -*- coding: utf-8 -*-
"""Module to parse incoming public messages from the exchange and store historial
data of the stocks in a Pandas DataFrame
"""

import pandas as pd

# Symbols
# BOND, VALBZ, VALE, GS, MS, WFC, XLF
# XLF: 3 BOND 2 GS 3 MS 2 WFC

symbols = ["BOND", "VALBZ", "VALE", "GS", "MS", "WFC", "XLF"]
price = pd.DataFrame(columns=symbols) # Trading Price of transation
volume = pd.DataFrame(columns=symbols) # Trading Volume of transaction
books = {}

def parse(message):
    if message["type"] == "trade":
        price.loc[price.shape[0], message["symbol"]] = float(message["price"])
        volume.loc[price.shape[0], message["symbol"]] = float(message["size"])

def backfill_data():
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    volume.fillna(method="ffill", inplace=True)
    volume.fillna(method="bfill", inplace=True)

def get_latest_price():
    backfill_data()
    latest_price = price.ix[price.shape[0]-1].to_dict()
    return latest_price

if __name__ == "__main__":
    import random
    for i in range(100):
        message = {"type": "trade",
                   "symbol": "BOND",
                   "price": random.randint(1000, 100000),
                   "size": random.randint(100000, 500000)}
        parse(message)
    print(get_latest_price())