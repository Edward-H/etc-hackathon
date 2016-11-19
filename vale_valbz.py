from parse_public_message import *


def trade_vale_valbz(id):
    (buy1, sell1) = get_books_mbms("VALE")
    (buy2, sell2) = get_books_mbms("VALBZ")
    if((not buy1) or (not sell1) or (not buy2) or (not sell2)):
        return
    if(buy1 - sell2 >= 20 and buy1 - sell2 < 100):
        write(exchange, {"type": "add", "order_id": id, "symbol":
              "VALBZ", "dir": "BUY", "price": sell2, "size": 1})
        write(
            exchange, {"type": "add", "order_id": id + 1, "symbol": "VALE", "dir": "SELL", "price": buy1, "size": 1})
        write(
            exchange, {"type": "convert", "order_id": id + 2, "symbol": "VALE", "dir": "BUY", "size": 1})
    elif(buy2 - sell1 >= 20 and buy2 - sell1 < 100):
        write(
            exchange, {"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "SELL", "price": buy2, "size": 1})
        write(
            exchange, {"type": "add", "order_id": id + 1, "symbol": "VALE", "dir": "BUY", "price": sell1, "size": 1})
        write(
            exchange, {"type": "convert", "order_id": id + 2, "symbol": "VALE", "dir": "SELL", "size": 1})



def trade_xlf (id)
    BOND_buy = sum(get_multi_books_mbms("BOND",3)[0])
    GS_buy = sum(get_multi_books_mbms("GS", 2)[0])
    MS_buy = sum(get_multi_books_mbms("MS", 3)[0])
    WFC_buy = sum(get_multi_books_mbms("WFC", 2)[0])
    XLF_sell = sum(get_books_mbms("XLF")[1])
    BOND_sell = sum(get_multi_books_mbms("BOND",3)[1])
    GS_sell = sum(get_multi_books_mbms("GS", 2)[1])
    MS_sell = sum(get_multi_books_mbms("MS", 3)[1])
    WFC_sell = sum(get_multi_books_mbms("WFC", 2)[1])
    XLF_buy = sum(get_books_mbms("XLF")[0])
    total_buy = BOND_buy + GS_buy + MS_buy + WFC_buy
    total_sell = BOND_sell + GS_sell + MS_sell + WFC_sell
    if(XLF_buy-total_sell>120 && XLF_buy-total_sell<1000):
        write(exchange, {"type": "add", "order_id": id, "symbol":
              "BOND", "dir": "BUY", "price": BOND_sell/3, "size": 3})
        write(exchange, {"type": "add", "order_id": id+1, "symbol":
              "GS", "dir": "BUY", "price": GS_sell/2, "size": 2})
        write(exchange, {"type": "add", "order_id": id+2, "symbol":
              "MS", "dir": "BUY", "price": MS_sell/3, "size": 3})
        write(exchange, {"type": "add", "order_id": id+3, "symbol":
              "WFC", "dir": "BUY", "price": WFC_sell/2, "size": 2})
        write(exchange, {"type": "add", "order_id": id+4, "symbol":
              "XLF", "dir": "SELL", "price": XLF_buy, "size": 1})
        write(exchange, {"type": "convert", "order_id": id+5, "symbol":
              "XLF", "dir": "BUY", "size": 1})
    elif(total_buy-XLF_sell>120 && total_buy-XLF_sell<1000):
        write(exchange, {"type": "add", "order_id": id, "symbol":
          "BOND", "dir": "SELL", "price": BOND_buy/3, "size": 3})
        write(exchange, {"type": "add", "order_id": id+1, "symbol":
            "GS", "dir": "SELL", "price": GS_buy/2, "size": 2})
        write(exchange, {"type": "add", "order_id": id+2, "symbol":
            "MS", "dir": "SELL", "price": MS_buy/3, "size": 3})
        write(exchange, {"type": "add", "order_id": id+3, "symbol":
            "WFC", "dir": "SELL", "price": WFC_buy/2, "size": 2})
        write(exchange, {"type": "add", "order_id": id+4, "symbol":
            "XLF", "dir": "BUY", "price": XLF_sell, "size": 1})
        write(exchange, {"type": "convert", "order_id": id+5, "symbol":
            "XLF", "dir": "SELL", "size": 1})
