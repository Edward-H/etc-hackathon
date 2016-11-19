#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import pdb

from vale_valbz import *
from parse_public_message import *

bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_bank = {"BOND": 0, "VALBZ": 0, "VALE":
                0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_orders = []
unverified_orders = []
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
    elif message["type"] == "reject":
        for order in range(len(unverified_orders)):
            if order.id == message["order_id"]:
                unverified_orders.remove(order)
    elif message["type"] == "ack":
        for order in unverified_orders:
            if order.id == message["order_id"]:
                pending_orders.append(order)
                unverified_orders.remove(order)


def update_orders():
    for order in pending_orders:
        if order.size == 0:
            pending_orders.remove(order)


def update_bond_holdings():
    # TO-DO: Cancel orders when impossible/better options exist.
    # Update the book if no orders are pending
    global trade_id
    trade_id += 1
    if pending_bank["BOND"] < 100 and bank["BOND"] < 100:
        order = Order(trade_id, "BOND", True, 999, 100 - pending_bank["BOND"])
        order.add()
        pending_orders.append(order)
    elif pending_bank["BOND"] > 0 and bank["BOND"] > 0:
        order = Order(trade_id, "BOND", False, 1001, bank["BOND"])
        order.add()
        pending_orders.append(order)


def trade_stock(stock):
    est = get_estimate_price(stock)
    (buy, sell) = get_books_msmb(stock)
    global trade_id
    trade_id += 1
    if(est > (sell + buy) / 2):
        order = Order(trade_id, stock, True, (sell + buy) / 2, 10)
        if(bank[stock] + pending_bank[stock] <= 90):
            order.add()
            unverified_orders.append(order)
    elif(est < (sell + buy) / 2):
        order = Order(trade_id, stock, False, (sell + buy) / 2, 10)
        if(bank[stock] + pending_bank[stock] >= -90):
            unverified_orders.append(order)


def main():
    global exchange
    global trade_id
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CARROT"})
    try:
        while True:
            exchange_msg = read(exchange)
            public_parse(exchange_msg)
            private_parse(exchange_msg)
            update_orders()
            update_bond_holdings()
            trade_id+=1
            trade_vale_valbz(trade_id)
            trade_id+=3
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
