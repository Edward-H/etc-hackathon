#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

from parse_public_message import *

bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_orders = []
trade_id = 0

def get_historical_points(stock):
    last_20_price = price[stock].dropna().tail(20)

def convert(id, stock, dir, size):
    if dir == True:
        b = "BUY"
    else:
        b = "SELL"
    write(exchange,
          {"type": "convert", "order_id": id, "symbol": stock, "dir": b, "size": size})

class Order(object):
    id = 0
    stock = ""
    dir = True
    price = 0
    size = 0

    def __init__(self, id, stock, dir, price, size):
        self.id = id
        self.stock = stock
        self.dir = dir
        self.price = price
        self.size = size

    def __str__(self):
        return "<{0}, {1}, {2}, {3}, {4}>".format(self.id, self.stock, self.dir, self.price, self.size)

    def add():
        b = ""
        if dir == True:
            b = "BUY"
        else:
            b = "SELL"
        write(exchange, {"type": "add", "order_id": id, "symbol":
              stock, "dir": b, "price": price, "size": size})

    def cancel():
        write(exchange, {"type": "cancel", "order_id": id})
        if(dir==True):
            bank[stock]-=size
        else:
            bank[stock]+=size

    def fill(fill_size):
        size -= fill_size
        if(dir == True):
            bank[stock] += fill_size
        else:
            bank[stock] -= fill_size

    def cancel():
        write(exchange, {"type": "cancel", "order_id": id})
        if(dir == True):
            bank[stock] -= size
        else:
            bank[stock] += size


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-carrot", 25001))
    return s.makefile('rw', 1)


def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read(exchange):
    return json.loads(exchange.readline())

def private_parse(message):
    if message["type"] == "fill":
        for order in pending_orders:
            if order.id == message["order_id"]:
                order.fill(message["size"])

def update_orders():
    for order in pending_orders:
        if order.size == 0:
            pending_orders.remove(order)

def update_bond_holdings():
    # TO-DO: Cancel orders when impossible/better options exist.
    # Update the book if no orders are pending
    if not [x for x in pending_orders if x.stock == "BOND"]:
        global trade_id
        trade_id += 1
        if bank["BOND"] == 0:
            order = Order(trade_id, "BOND", True, 1000, 100)
            order.add
            pending_orders.append(order)
        else:
            order = Order(trade_id, "BOND", False, 1001, bank["BOND"])
            order.add
            pending_orders.append(order)

def main():
    global exchange
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CARROT"})
    try:
        while True:
            exchange_msg = read(exchange)
            public_parse(exchange_msg)
            private_parse(exchange_msg)
            update_orders()
            update_bond_holdings()
            print(bank)
            for order in pending_orders:
                print(order)
            print("\n")
    except KeyboardInterrupt:
        exchange.close()
        print(bank)

if __name__ == "__main__":
    main()
