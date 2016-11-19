from parse_public_message import *


def trade_vale_valbz(id):
    (buy1,sell1) = get_books_mbms("VALE")
    (buy2,sell2) = get_books_mbms("VALBZ")
    if(buy1-sell2>=20):
        write(exchange,{"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "BUY", "price": sell2, "size": 1})
        write(exchange,{"type": "add", "order_id": id+1, "symbol": "VALE", "dir": "SELL", "price": buy1, "size": 1})
        write(exchange,{"type": "convert", "order_id": id+2, "symbol": "VALE", "dir": "BUY", "size": 1})
    else if(buy2-sell1>=20):
        write(exchange,{"type": "add", "order_id": id, "symbol": "VALBZ", "dir": "SELL", "price": buy2, "size": 1})
        write(exchange,{"type": "add", "order_id": id+1, "symbol": "VALE", "dir": "BUY", "price": sell1, "size": 1})
        write(exchange,{"type": "convert", "order_id": id+2, "symbol": "VALE", "dir": "SELL", "size": 1})

=======
