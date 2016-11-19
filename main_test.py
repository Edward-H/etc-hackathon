#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import pdb
import time

from parse_public_message import *
import time

bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_bank_min = {"BOND": 0, "VALBZ": 0, "VALE":
                0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
pending_bank_max = {"BOND": 0, "VALBZ": 0, "VALE":
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
            pending_bank_max[self.stock] += self.size
        else:
            b = "SELL"
            pending_bank_min[self.stock] -= self.size
        write(exchange, {"type": "add", "order_id": self.id, "symbol":
              self.stock, "dir": b, "price": self.price, "size": self.size})

    def cancel(self):
        write(exchange, {"type": "cancel", "order_id": self.id})
        if(self.dir == True):
            bank[self.stock] -= self.size
            pending_bank_max -= self.size
        else:
            bank[self.stock] += self.size
            pending_bank_min += self.size

    def fill(self, fill_size):
        self.size -= fill_size
        if(self.dir == True):
            bank[self.stock] += fill_size
            pending_bank_min[self.stock] += fill_size
        else:
            bank[self.stock] -= fill_size
            pending_bank_max[self.stock] -= fill_size

    def cancel(self):
        write(exchange, {"type": "cancel", "order_id": self.id})
        if(self.dir == True):
            bank[self.stock] -= self.size
        else:
            bank[self.stock] += self.size

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-carrot", 25000))
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
        for order in unverified_orders:
            if order.id == message["order_id"]:
                if message["error"] == "LIMIT:POSITION":
                    print("----------------------------")
                    print(pending_orders)
                    print(unverified_orders)
                    print(pending_bank_max)
                    print(pending_bank_min)
                    print(order)
                    raise "Argh!"

                unverified_orders.remove(order)
                if order.dir == True:
                    pending_bank_max[order.stock] -= order.size
                else:
                    pending_bank_min[order.stock] += order.size
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
    if pending_bank_max["BOND"] < 100:
        order = Order(trade_id, "BOND", True, 999, 100 - pending_bank_max["BOND"])
        order.add()
        unverified_orders.append(order)
    elif pending_bank_min["BOND"] > 0:
        order = Order(trade_id, "BOND", False, 1001, bank["BOND"])
        order.add()
        unverified_orders.append(order)

# def trade_stock(stock):
#     est = get_estimate_price(stock)
#     (buy, sell) = get_books_msmb(stock)
#     global trade_id
#     trade_id += 1
#     if(est > (sell + buy) / 2):
#         order = Order(trade_id, stock, True, (sell + buy) / 2, 10)
#         if(bank[stock] + pending_bank[stock] <= 90):
#             order.add()
#             unverified_orders.append(order)
#     elif(est < (sell + buy) / 2):
#         order = Order(trade_id, stock, False, (sell + buy) / 2, 10)
#         if(bank[stock] + pending_bank[stock] >= -90):
#             unverified_orders.append(order)


def trade_vale_valbz(id):
    (buy1, sell1) = get_books_mbms("VALE")
    (buy2, sell2) = get_books_mbms("VALBZ")
    if((not buy1) or (not sell1) or (not buy2) or (not sell2)):
        return
    if(buy1 - sell2 >= 15 and buy1 - sell2 < 1000):
        write(exchange, {"type": "add", "order_id": id, "symbol":
              "VALBZ", "dir": "BUY", "price": sell2, "size": 1})
        write(
            exchange, {"type": "add", "order_id": id + 1, "symbol": "VALE", "dir": "SELL", "price": buy1, "size": 1})
        write(
            exchange, {"type": "convert", "order_id": id + 2, "symbol": "VALE", "dir": "BUY", "size": 1})
    elif(buy2 - sell1 >= 15 and buy2 - sell1 < 1000):
        write(
            exchange, {"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "SELL", "price": buy2, "size": 1})
        write(
            exchange, {"type": "add", "order_id": id + 1, "symbol": "VALE", "dir": "BUY", "price": sell1, "size": 1})
        write(
            exchange, {"type": "convert", "order_id": id + 2, "symbol": "VALE", "dir": "SELL", "size": 1})

def trade_xlf (id):
    try:
        BOND_buy = sum(get_multi_books_mbms("BOND",3)[0])
        GS_buy = sum(get_multi_books_mbms("GS", 2)[0])
        MS_buy = sum(get_multi_books_mbms("MS", 3)[0])
        WFC_buy = sum(get_multi_books_mbms("WFC", 2)[0])
        XLF_sell = sum(get_books_mbms("XLF")[1])*10
        BOND_sell = sum(get_multi_books_mbms("BOND",3)[1])
        GS_sell = sum(get_multi_books_mbms("GS", 2)[1])
        MS_sell = sum(get_multi_books_mbms("MS", 3)[1])
        WFC_sell = sum(get_multi_books_mbms("WFC", 2)[1])
        XLF_buy = sum(get_books_mbms("XLF")[0])*10
        total_buy = BOND_buy + GS_buy + MS_buy + WFC_buy
        total_sell = BOND_sell + GS_sell + MS_sell + WFC_sell
        if(XLF_buy-total_sell>120 and XLF_buy-total_sell<200):
            write(exchange, {"type": "add", "order_id": id, "symbol":
                  "BOND", "dir": "BUY", "price": BOND_sell/3, "size": 3})
            write(exchange, {"type": "add", "order_id": id+1, "symbol":
                "GS", "dir": "BUY", "price": GS_sell/2, "size": 2})
            write(exchange, {"type": "add", "order_id": id+2, "symbol":
                "MS", "dir": "BUY", "price": MS_sell/3, "size": 3})
            write(exchange, {"type": "add", "order_id": id+3, "symbol":
                "WFC", "dir": "BUY", "price": WFC_sell/2, "size": 2})
            write(exchange, {"type": "add", "order_id": id+4, "symbol":
                "XLF", "dir": "SELL", "price": XLF_buy, "size": 10})
            write(exchange, {"type": "convert", "order_id": id+5, "symbol":
                "XLF", "dir": "BUY", "size": 10})
        elif(total_buy-XLF_sell>120 and total_buy-XLF_sell<200):
            write(exchange, {"type": "add", "order_id": id, "symbol":
                  "BOND", "dir": "SELL", "price": BOND_buy/3, "size": 3})
            write(exchange, {"type": "add", "order_id": id+1, "symbol":
                        "GS", "dir": "SELL", "price": GS_buy/2, "size": 2})
            write(exchange, {"type": "add", "order_id": id+2, "symbol":
                        "MS", "dir": "SELL", "price": MS_buy/3, "size": 3})
            write(exchange, {"type": "add", "order_id": id+3, "symbol":
                        "WFC", "dir": "SELL", "price": WFC_buy/2, "size": 2})
            write(exchange, {"type": "add", "order_id": id+4, "symbol":
                        "XLF", "dir": "BUY", "price": XLF_sell, "size": 10})
            write(exchange, {"type": "convert", "order_id": id+5, "symbol":
                        "XLF", "dir": "SELL", "size": 10})
    except TypeError:
        print("none type error")

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
            trade_id += 1
            trade_vale_valbz(trade_id)
            trade_id += 3
            #trade_xlf(trade_id)
            #trade_id+=6
            print(exchange_msg)
            print(bank)
            print(pending_bank_max)
            print(pending_bank_min)
            for order in pending_orders:
                print(order)
            print("\n")
            time.sleep(0.05)
    except KeyboardInterrupt:
        exchange.close()
        print(bank)

if __name__ == "__main__":
    main()
