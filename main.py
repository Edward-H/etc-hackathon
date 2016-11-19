#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_order_list = []

class Order(object):
    id = 0
    stock = ""
    dir = true
    price = 0
    size = 0

    def __init__(self, id, stock, dir, price, size):
        self.id = id
        self.stock = stock
        self.dir = dir
        self.price = price
        self.size = size

    def make_order(id, stock, dir, price, size):
        order = Order(id, stock, dir, price, size)
        return order

    def add():
        b = ""
        if dir == true:
            b = "BUY"
        else:
            b = "SELL"
        write(exchange, {"type": "add", "order_id": id, "symbol":
              stock, "dir": b, "price": price, "size": size})

    def fill(fill_size):
        size -= fill_size
        if(dir == true):
            bank[stock] += fill_size
        else:
            bank[stock] -= fill_size

    def cancel():
        write(exchange, {"type": "cancel", "order_id": id})
        if(dir == true):
            bank[stock] -= size
        else:
            bank[stock] += size


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.1.245", 25000))
    return s.makefile('rw', 1)


def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read(exchange):
    return json.loads(exchange.readline())

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
            pending_orders.append(Order.make_order(trade_id, "BOND", True, 1000, 100))
        else:
            pending_orders.append(Order.make_order(trade_id, "BOND", False, 1001, bank["BOND"]))

def main():
    global exchange
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CARROT"})
    try:
        while True:
            parse(read(exchange))
            update_orders()
            update_bond_holdings()
    except KeyboardInterrupt:
        exchange.close()
        print(bank)

if __name__ == "__main__":
    main()
