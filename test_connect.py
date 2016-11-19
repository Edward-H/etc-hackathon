#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json 

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
    write(exchange, {"type": "hello", "team": "TEAMNAME"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    try:
        from parse_public_message import *
        exchange = connect()
        
        write(exchange, {"type": "hello", "team": "CARROT"})
        while price.shape[0] < 50:
            message = read(exchange)
            parse(message)
            print(get_latest_price())
        
        print(price)
        exchange.close()
    except KeyboardInterrupt:
        exchange.close()