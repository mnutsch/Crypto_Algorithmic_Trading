


# This is my exchange keys for Geminis Sandbox API
API_KEY = ''
SECRET_KEY = ''

from geminipy import Geminipy


def new_gemini_order(amount, price, side, symbol):

    con = Geminipy(api_key=API_KEY, secret_key=SECRET_KEY, live=False)

    order = con.new_order(amount=amount, price=price,side=side, symbol=symbol)

    return order.json()



# Example Usage

# print new_gemini_order('1', '3000', 'sell', 'btcusd')

# print new_gemini_order('1', '3000', 'buy', 'btcusd')
