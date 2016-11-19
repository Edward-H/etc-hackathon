#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json 
import numpy as np
from parse_public_message import *
from order import *
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-carrot", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

if __name__ == "__main__":
    try:
        exchange = connect()
        write(exchange, {"type": "hello", "team": "CARROT"})
        time.sleep(1)
        while True:
            message = read(exchange)
            if message["type"] == "trade" or message["type"] == "book":
                public_parse(message)
            elif message["type"] == "ack" or message["type"] == "reject" or message["type"] == "fill" or message["type"] == "out":
                parse_order_msg(message)
            else:
                print(message)
#            (buy1, sell1) = get_books_mbms("VALE")
#            (buy2, sell2) = get_books_mbms("VALBZ")
#            if buy1 != None and buy2 != None and sell1 != None and sell2 != None:
#                if buy1 - sell2 >= 15:
#                    add_order(exchange, "VALBZ", True, sell2, 1)
#                    add_order(exchange, "VALE", False, buy1, 1)
#                    convert_order(exchange, "VALE", 1)
#                if buy2 - sell1 >= 15:
#                    add_order(exchange, "VALBZ", False, buy2, 1)
#                    add_order(exchange, "VALE", True, sell1, 1)
#                    convert_order(exchange, "VALBZ", 1)
            BOND_buy = sum(get_multi_books_mbms("BOND",3)[0])
            GS_buy = sum(get_multi_books_mbms("GS", 2)[0])
            MS_buy = sum(get_multi_books_mbms("MS", 3)[0])
            WFC_buy = sum(get_multi_books_mbms("WFC", 2)[0])
            XLF_sell = sum(get_books_mbms("XLF")[1])
            total_buy = BOND_buy + GS_buy + MS_buy + WFC_buy
        
    except KeyboardInterrupt:
        exchange.close()