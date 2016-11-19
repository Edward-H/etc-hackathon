#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json 

def add(id,stock,dir,price,size)
    if(dir==true) b="BUY"
    else b="SELL"
    write(exchange,{"type": "add", "order_id": id, "symbol": stock, "dir": b, "price": price, "size": size})

def convert(id,stock,dir,size)
    if(dir==true) b="BUY"
    else b="SELL"
    {"type": "convert", "order_id": id, "symbol": stock, "dir": b, "size": size}

def cancel(id)
    {"type": "cancel", "order_id": id}

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
