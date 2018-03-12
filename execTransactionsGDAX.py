import gdax


# These are only for GDAX sandbox API
key = ''
b64secret = ''
passphrase = ''


def new_gdax_order(amount, price, side, symbol):

    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase, api_url="https://api-public.sandbox.gdax.com")

    if side == 'buy':
        print auth_client.buy(price=price, size=amount, product_id=symbol)
    elif side == 'sell':
        print auth_client.sell(price=price, size=amount, product_id=symbol)


### Example calls

# new_gdax_order('1', '10000', 'buy', 'BTC-USD')

# # new_gdax_order('1', '10000', 'sell', 'BTC-USD')