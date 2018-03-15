# Name: exchange.py
# Author: Patrick Mullaney
# Date Created: 3-1-2018
# Last Edited: 3-10-2018
# Description: This file provides functions for exchange objects.

import currency

# Exchange object contains information relevant to a currency at that exchange.    
class Exchange(): 
    name = None
    currency = None
    price = None
    depositFee = None
    withdrawFee = None
    exchangeFee = None
    volume = 0.00

################################################################################

# Returns currency info at a given exchange.
def getExchange(xchg, curr):
    exchgInfo = Exchange()
    exchgInfo.name = xchg
    exchgInfo.currency = curr
    exchgInfo.price = currency.getPrice(xchg, curr)
    exchgInfo.depositFee = currency.getDepositFee(xchg, curr)
    exchgInfo.withdrawFee = currency.getWithdrawFee(xchg, curr)
    exchgInfo.exchangeFee = currency.getExchangeFee(xchg, curr)
    return exchgInfo
    
################################################################################

# Returns currency info at a given exchange.
def getExchange1(xchg, curr):
    exchgInfo = Exchange()
    exchgInfo.name = xchg
    exchgInfo.currency = curr
    exchgInfo.price = currency.getPrice(xchg, curr)
    exchgInfo.depositFee = getDepositFee(xchg, curr)
    exchgInfo.withdrawFee = currency.getWithdrawFee(xchg, curr)
    exchgInfo.exchangeFee = currency.getExchangeFee(xchg, curr)
    return exchgInfo

################################################################################

# Returns deposit % fee for a currency at a given exchange (currently no fees).
def getDepositFee(xchg, curr):
    fee = 0
    if xchg == 'gdax':
        if curr == 'BCH':
            fee = 0.00
        elif curr == 'ETH':
            fee = 0.00
        elif curr == 'LTC':
            fee = 0.00
        elif curr == 'BTC':
            fee = 0.00
    elif xchg == 'gemini':
        if curr == 'BTC':
            fee = 0.00
        elif curr == 'ETH':
            fee = 0.00
    return fee

################################################################################
