# -*- coding: utf-8 -*-
"""Module to add orders, parse order messages and track orders"""

import pandas as pd
import json

order_columns = ["Symbol", "Type", "Price", "Size"]
sent_orders = pd.DataFrame(columns=order_columns)
book_orders = pd.DataFrame(columns=order_columns)

bank = {"Cash": 0,
        "BOND": 0,
        "VALBZ": 0,
        "VALE": 0,
        "GS": 0,
        "MS": 0,
        "WFC": 0,
        "XLF": 0}

order_id = 0

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def get_order_id():
    global order_id
    order_id += 1
    return order_id

def add_order(exchange, symbol, buy, price, size):
    oid = get_order_id()
    buysell = ""
    if buy == True:
        buysell = "BUY"
    else:
        buysell = "SELL"
    write(exchange, {"type": "add", "order_id": oid,
                     "symbol": symbol, "dir": buysell,
                     "price": price, "size": size})
    sent_orders.loc[oid] = [symbol, buysell, price, size]

def cancel_order(exchange, oid):
    write(exchange, {"type": "cancel", "order_id": oid})

def convert_order(exchange, symbol, size):
    oid = get_order_id()
    write(exchange, {"type": "convert", "order_id": oid,
                     "symbol": symbol, "dir": "BUY", "size": size})
    sent_orders.loc[oid] = [symbol, "CONVERT", 0, size]

def parse_order_msg(msg):
    oid = msg["order_id"]
    if msg["type"] == "ack":
        if sent_orders.loc[oid, "Type"] == "CONVERT":
            if sent_orders.loc[oid, "Symbol"] == "VALE":
                bank["VALE"] += sent_orders.loc[oid, "Size"]
                bank["VALBZ"] -= sent_orders.loc[oid, "Size"]
            elif sent_orders.los[oid, "Symbol"] == "VALBZ":
                bank["VALE"] -= sent_orders.loc[oid, "Size"]
                bank["VALBZ"] += sent_orders.loc[oid, "Size"]
            bank["Cash"] -= 10*sent_orders.loc[oid, "Size"];
        else:
            book_orders.loc[oid] = sent_orders.loc[oid]
        sent_orders.drop(oid)
    elif msg["type"] == "reject":
        sent_orders.drop(oid)
    elif msg["type"] == "fill":
        print("{} {} shares of {} at ${}".format(msg["dir"],msg["size"],msg["symbol"],msg["price"]))
        print(bank)
        book_orders.loc[oid, "Size"] = book_orders.loc[oid, "Size"] - msg["size"]
        if msg["dir"] == "BUY":
            bank[msg["symbol"]] += msg["size"]
            bank["Cash"] -= msg["size"]*msg["price"]
        elif msg["dir"] == "SELL":
            bank[msg["symbol"]] -= msg["size"]
            bank["Cash"] += msg["size"]*msg["price"]
    elif msg["type"] == "out":
        book_orders.drop(oid)