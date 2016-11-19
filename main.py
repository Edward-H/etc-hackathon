#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

bank = {"money": 0, "BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}


def add(id, stock, dir, price, size):
    b = ""
    if dir == true:
        b = "BUY"
    else:
        b = "SELL"
    write(exchange, {"type": "add", "order_id": id, "symbol":
          stock, "dir": b, "price": price, "size": size})


def convert(id, stock, dir, size):
    if dir == true:
        b = "BUY"
    else:
        b = "SELL"
    write(exchange,
          {"type": "convert", "order_id": id, "symbol": stock, "dir": b, "size": size})



from parse_public_message import *

def cancel(id):
    write(exchange, {"type": "cancel", "order_id": id})

import pandas as pd

# Symbols
# BOND, VALBZ, VALE, GS, MS, WFC, XLF
# XLF: 3 BOND 2 GS 3 MS 2 WFC

symbols = ["BOND", "VALBZ", "VALE", "GS", "MS", "WFC", "XLF"]
price = pd.DataFrame(columns=symbols)  # Trading Price of transation
volume = pd.DataFrame(columns=symbols)  # Trading Volume of transaction
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
    latest_price = price.ix[price.shape[0] - 1].to_dict()
    return latest_price
>>>>>>> origin/master


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-carrot", 25000))
    return s.makefile('rw', 1)


def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read(exchange):
    return json.loads(exchange.readline())


def main():
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CARROT"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
