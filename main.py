#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import pdb

from parse_public_message import *

bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_bank = {"BOND": 0, "VALBZ": 0, "VALE":
                0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
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

    def add(self):
        b = ""
        if self.dir == True:
            b = "BUY"
            pending_bank[self.stock] += self.size
        else:
            b = "SELL"
            pending_bank[self.stock] -= self.size
        write(exchange, {"type": "add", "order_id": self.id, "symbol":
              self.stock, "dir": b, "price": self.price, "size": self.size})

    def cancel(self):
        write(exchange, {"type": "cancel", "order_id": self.id})
        if(self.dir == True):
            bank[self.stock] -= self.size
        else:
            bank[self.stock] += self.size

    def fill(self, fill_size):
        self.size -= fill_size
        if(self.dir == True):
            bank[self.stock] += fill_size
        else:
            bank[self.stock] -= fill_size

    def cancel(self):
        write(exchange, {"type": "cancel", "order_id": self.id})
        if(self.dir == True):
            bank[self.stock] -= self.size
        else:
            bank[self.stock] += self.size


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
    global trade_id
    trade_id += 1
    if pending_bank["BOND"] == 0:
        order = Order(trade_id, "BOND", True, 1000, 100)
        order.add()
        pending_orders.append(order)
    else:
        order = Order(trade_id, "BOND", False, 1001, bank["BOND"])
        order.add()
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
            print(pending_bank)
            for order in pending_orders:
                print(order)
            print("\n")
    except KeyboardInterrupt:
        exchange.close()
        print(bank)

if __name__ == "__main__":
    main()
