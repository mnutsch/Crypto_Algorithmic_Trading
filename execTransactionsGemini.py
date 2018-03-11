


# This is my exchange keys for Geminis Sandbox API
API_KEY = 'AX1tbzYLU178pyIJ75M4'
SECRET_KEY = '3tRZ1YhzghnFAXFiJx5fKBY5BPFS'

from geminipy import Geminipy


def new_gemini_order(amount, price, side, symbol):

    con = Geminipy(api_key=API_KEY, secret_key=SECRET_KEY, live=False)

    order = con.new_order(amount=amount, price=price,side=side, symbol=symbol)

    return order.json()



# Example Usage

# print new_gemini_order('1', '3000', 'sell', 'btcusd')

# print new_gemini_order('1', '3000', 'buy', 'btcusd')
