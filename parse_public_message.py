# -*- coding: utf-8 -*-
"""Module to parse incoming public messages from the exchange and store historial
data of the stocks in a Pandas DataFrame
"""

import pandas as pd

# Symbols
# BOND, VALBZ, VALE, GS, MS, WFC, XLF
# XLF: 3 BOND 2 GS 3 MS 2 WFC

symbols = ["BOND", "VALBZ", "VALE", "GS", "MS", "WFC", "XLF"]
price = pd.DataFrame(columns=symbols)  # Trading Price of transation
price.loc[0] = [0, 0, 0, 0, 0, 0, 0]
volume = pd.DataFrame(columns=symbols)  # Trading Volume of transaction
volume.loc[0] = [0, 0, 0, 0, 0, 0, 0]
books = {}
for symbol in symbols:
    books[symbol] = {"buy": [], "sell": []}


def backfill_data():
#    price.fillna(method="ffill", inplace=True)
#    price.fillna(method="bfill", inplace=True)
#    volume.fillna(method="ffill", inplace=True)
#    volume.fillna(method="bfill", inplace=True)
    pass


def parse(message):
    if message["type"] == "trade":
        price.loc[price.shape[0], message["symbol"]] = float(message["price"])
        volume.loc[price.shape[0], message["symbol"]] = float(message["size"])
    elif message["type"] == "book":
        books[message["symbol"]] = {
            "buy": message["buy"], "sell": message["sell"]}
    backfill_data()


def get_latest_price():
    backfill_data()
    latest_price = price.ix[price.shape[0] - 1].to_dict()
    return latest_price


def get_rolling_mean(period=20):
    r_mean = price.rolling(period).mean()
    return r_mean.loc[r_mean.shape[0] - 1].to_dict()


def get_rolling_std(period=20):
    r_std = price.rolling(period).std()
    return r_std.loc[r_std.shape[0] - 1].to_dict()


def get_sharpe_ratio(period=20):  # Not actually sharpe's ratio
    cum_returns = (price.loc[price.shape[0] - 1] / price.loc[
                   max(0, price.shape[0] - period - 1)]) - 1
    stdev = price.rolling(period).std()
    sharpe_ratio = cum_returns / stdev
    return sharpe_ratio.loc[sharpe_ratio.shape[0] - 1].to_dict()


def get_latest_volume():
    backfill_data()
    latest_vol = volume.loc[volume.shape[0] - 1].to_dict()
    return latest_vol


def get_latest_books():
    return books

if __name__ == "__main__":
    import random
    for i in range(100):
        message = {"type": "trade",
                   "symbol": "BOND",
                   "price": random.randint(1000, 100000),
                   "size": random.randint(100000, 500000)}
        parse(message)
    print(get_latest_price())
    print(get_latest_volume())
    print(get_rolling_mean())
    print(get_rolling_std())
    print(get_sharpe_ratio())
