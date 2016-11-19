#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

<<<<<<< HEAD
bank = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}



class Order(object):
    id=0
    stock=""
    dir=true
    price=0
    size=0
    
    def __init__(self,id,stock,dir,price,size):
        self.id=id
        self.stock=stock
        self.dir=dir
        self.price=price
        self.size=size
        
    def make_order(id,stock,dir,price,size):
        order = Order(id,stock,dir,price,size)
        return order

    def add():
        b = ""
        if dir == true:
            b = "BUY"
        else:
            b = "SELL"
        write(exchange, {"type": "add", "order_id": id, "symbol":
              stock, "dir": b, "price": price, "size": size})

    def ack():
        if(dir==true) bank[stock]+=size
        else bank[stock]-=size

    def cancel():
        write(exchange, {"type": "cancel", "order_id": id})
        if(dir==true) bank[stock]-=size
        else bank[stock]+=size
=======
from parse_public_message import *

bank = {"money": 0, "BOND": 0, "VALBZ": 0,
        "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
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


>>>>>>> origin/master


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.1.245", 25000))
    return s.makefile('rw', 1)


def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read(exchange):
    return json.loads(exchange.readline())


def update_bond_holdings():
    # TO-DO: Cancel orders when impossible/better options exist.
    global trade_id
    current_bond_price = get_latest_price()["BOND"]
    if current_bond_price > 1000 and bank["BOND"] > 0:
        # Sell bonds (if we have any) if they are more than 1000.
        trade_id += 1
        add(trade_id, "BOND", False, current_bond_price +
            1, min(bank["BOND"], entry.size))
    elif current_bond_price < 1000 and bank["BOND"] < 100:
        # Buy more bonds (if we can) if they are less than 1000.
        trade_id += 1
        add(trade_id, "BOND", True, current_bond_price - 1, 100 - bank["BOND"])


def main():
    global exchange
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CARROT"})
    try:
        while True:
            parse(read(exchange))
            update_bond_holdings()
    except KeyboardInterrupt:
        exchange.close()
        print(bank)

if __name__ == "__main__":
    main()
