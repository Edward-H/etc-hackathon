from parse_public_message import *


def trade_vale_valbz(id):
    (buy1,sell1) = get_books_mbms("VALE")
    (buy2,sell2) = get_books_mbms("VALBZ")
    if((not buy1) or (not sell1) or (not buy2) or (not sell2) ): return
    if(buy1-sell2>=20 && buy1-sell2<100):
        write(exchange,{"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "BUY", "price": sell2, "size": 1})
        write(exchange,{"type": "add", "order_id": id+1, "symbol": "VALE", "dir": "SELL", "price": buy1, "size": 1})
        write(exchange,{"type": "convert", "order_id": id+2, "symbol": "VALE", "dir": "BUY", "size": 1})
<<<<<<< HEAD
    else if(buy2-sell1>=20 && buy2-sell1<100):
=======
    elif(buy2-sell1>=20):
>>>>>>> origin/master
        write(exchange,{"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "SELL", "price": buy2, "size": 1})
        write(exchange,{"type": "add", "order_id": id+1, "symbol": "VALE", "dir": "BUY", "price": sell1, "size": 1})
        write(exchange,{"type": "convert", "order_id": id+2, "symbol": "VALE", "dir": "SELL", "size": 1})
