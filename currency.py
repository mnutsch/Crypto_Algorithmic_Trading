# Name: currency.py
# Author: Patrick Mullaney
# Date Created: 3-7-2018
# Last Edited: 3-11-2018
# Description: This file contains functions related to currencies, return a list of currencies, etc.

# File for calculations.
import calc
import readExchangeRatesGDAX, readExchangeRatesGemini

#*** Volume amounts are hardcoded test values to simulate trading 
#   without financial implications during development ***.

# Object containing information about a currency.
class Currency():
    name = None,
    exchange = None,
    amount = 0.00,
    volume = 0
    cost = 0.00,
    price = 0.00
    depositFee = 0.00
    exchangeFee = 0.00
    withdrawFee = 0.00

# From SO: https://stackoverflow.com/questions/5969806/print-all-properties-of-a-python-class- used only for debuggging.   
def printCurr(curr):
    attrs = vars(curr)
    print ', '.join("%s: %s" % item for item in attrs.items())

################################################################################

# Returns withdraw fee for a currency at a given exchange (original in single currency.py).
def getWithdrawFee(xchg, curr):
    if xchg == 'gdax':
        fee = 0.00
    elif xchg == 'gemini':
        if curr == 'BTC':
            #fee = 1.002 # Review, fees may apply for 10+ trades/month.
            fee = 0.00
        elif curr == 'ETH':
            fee = 0.00
    return fee

################################################################################

# Returns users trade volume.
def getUserVolume(curr):
    if curr == 'BTC':
        volume = 151694.90
    elif curr == 'BCH':
        volume = 85912.65
    elif curr == 'ETH':
        volume = 85814059
    elif curr == 'LTC':
        volume = 4747224.13
    return volume
    
################################################################################

# Returns user trade volume % for a currency at gdax.
def gdaxUserVol(curr, volume):
    # 30 day volume hard coded for testing and demonstration purposes to not incur financial losses during development.
    if curr == 'BTC':
        vol30day = 753474.52 
    elif curr == 'BCH':
        vol30day = 424563.26
    elif curr == 'ETH':
        vol30day = 4190702.95
    elif curr == 'LTC':
        vol30day = 18736120.64
    # Calculate and return user's volume %.
    userVol = (volume/vol30day) * 100
    return userVol

################################################################################

# Returns exchange fee for a currency at an exchange.
def getExchangeFee(exchange, curr):
    # Get user's volume, which will determine exchange fee pricing.
    volume = getUserVolume(curr)
    if exchange is "gdax":
        # Gdax uses a volume percentage for fees, get user percentage.
        userVol = gdaxUserVol(curr, volume)
        if userVol >= 0.0 and userVol <= 1.0:
            # BTC is only currency that has different fee %.
            if curr == 'BTC':
                fee = 0.25
            else:
                fee = 0.3
        elif userVol > 1.0 and userVol <= 2.5:
            fee = 0.24
        elif userVol > 2.5 and userVol <= 5.0:
            fee = 0.22
        elif userVol > 5.0 and userVol <= 10.0:
            fee = 0.19
        elif userVol > 10.0 and userVol <= 20.0:
            fee = 0.15
        elif userVol > 20.0:
            fee = 0.1
    elif exchange is "gemini":
        if curr == 'BTC':
            if volume >= 0 and volume < 1000:
                fee = 0.25
            elif volume >= 1000 and volume < 2000:
                fee = 0.23
            elif volume >= 2000 and volume < 3000:
                fee = .2
            elif volume >= 3000 and volume < 5000:
                fee = .15
            elif volume >= 5000:
                fee = .10
        elif curr == 'ETH':
            if volume >= 0 and volume < 20000:
                fee = 0.25
            elif volume >= 20000 and volume < 40000:
                fee = 0.23
            elif volume >= 40000 and volume < 60000:
                fee = .2
            elif volume >= 60000 and volume < 100000:
                fee = .15
            elif volume >= 100000:
                fee = .10
    return fee

################################################################################

# Returns a currency object with name and price initialized.
def getCurrency(name, exchange):
    curr = Currency()
    curr.volume = getUserVolume(name)
    curr.name = name
    curr.exchange = exchange
    curr.price = getPrice(exchange, curr.name)
    curr.depositFee = getDepositFee(exchange, curr.name)
    curr.exchangeFee = getExchangeFee(exchange, curr.name)
    curr.withdrawFee = getWithdrawFee(exchange, curr.name)
    return curr

################################################################################

# Returns deposit % fee for a currency at a given exchange.
def getDepositFee(xchg, curr):
    if xchg == 'gdax':
        if curr == 'BCH' or curr == 'LTC':
            fee = 0.00
        elif curr == 'ETH' or curr == 'BTC':
            fee = 0.001
    elif xchg == 'gemini':
        fee = 0.001
    else:
        print "No match: ", xchg, curr
    return fee

################################################################################

# Returns price of a currency at a given exchange.
def getPrice(xchg, curr):
    # Gdax pricing
    if xchg == 'gdax':
        if curr == 'BCH':
            price = float(readExchangeRatesGDAX.getBCHToUSDFromGDAX())
        elif curr == 'ETH':
            price = float(readExchangeRatesGDAX.getETHToUSDFromGDAX())
        elif curr == 'LTC':
            price = float(readExchangeRatesGDAX.getLTCToUSDFromGDAX())
        elif curr == 'BTC':
            price = float(readExchangeRatesGDAX.getBTCToUSDFromGDAX())
    # Gemini pricing
    elif xchg == 'gemini':
        if curr == 'BTC':
            price = float(readExchangeRatesGemini.getBTCToUSDFromGemini())
        elif curr == 'ETH':
            price = float(readExchangeRatesGemini.getETHToUSDFromGemini())
    return price

################################################################################

# Returns list of currency objects.
def getCurrencyList():
    btc = getCurrency('BTC', 'gdax')
    eth = getCurrency('ETH', 'gdax')
    ltc = getCurrency('LTC', 'gdax')
    bch = getCurrency('BCH', 'gdax')
    btcGem = getCurrency('BTC', 'gemini')
    ethGem = getCurrency('ETH', 'gemini')
    currencyList = [btc, eth, ltc, bch, btcGem, ethGem]
    #currencyList = [btc, eth, ltc, bch] # Only used gdax during initial testing.
    return currencyList

################################################################################

# Returns fee cost of buying an amount of currency.
def getCost(curr, amount):
    fee = getExchangeFee(curr.exchange, curr.name)
    cost = (amount * curr.price * fee)/100.00
    return cost

################################################################################

# Returns cost of a % fee for a currency.
def getFeeCost(curr, fee):
    feeCost = float(100.00 - fee)/100.00
    return feeCost