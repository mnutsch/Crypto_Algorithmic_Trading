# Name: calc.py
# Author: Patrick Mullaney
# Date Created: 2-8-2018
# Last Edited: 2-17-2018
# Description: This script checks contains calculation functions that can
# be used by checkSingleCurrencyOpps.py and checkMultipleCurrencyOpps.py.

#### Review: GEMINI does not support LTC/BCH

import readExchangeRatesGDAX, readExchangeRatesGemini

# Number of pairwise comparisons = n(n-1)/2, for N = 12, comparisons = 66.

# Compares 3 currency conversion costs and returns true if there is a potentially profitable chain.  
# Example use: if ([BTC to ETH] > [ETH to LTC]) and ([LTC to BTC] < [ETH to LTC]), then buy ETH with BTC, buy LTC with ETH and buy BTC with LTC. 
def checkThree(cost1, cost2, cost3):
    if(cost1 > cost2) and (cost3 < cost2):
        return True
    else:
        return False

# Opportunity object stores the potential info about an exchange.
class Opportunity():
    currency = None
    buyExchange = None
    sellExchange = None
    buyPrice = None
    sellPrice = None
    amount = None
    profitLoss = 0.00

# Exchange object contains information relevant to that exchange.    
class Exchange(): 
    name = None
    currency = None
    price = None
    depositFee = None
    withdrawFee = None
    exchangeFee = None
    # Add different fees for maker/taker?

# Calculates revenue with deposit and withdraw fee costs.
def calcRev1(amount, lowPrice, highPrice, exchangeCostLow, exchangeCostHigh, depositCost, withdrawCost):
    revenue = ((amount * lowPrice) * depositCost)/lowPrice * exchangeCostLow * highPrice * exchangeCostHigh * withdrawCost
    return revenue
    
# Calculates revenue without deposit and withdraw fee costs.
def calcRev2(amount, lowPrice, highPrice, exchangeFeeLow, exchangeFeeHigh):
    revenue = (amount * highPrice * exchangeFeeHigh) - (amount * lowPrice * exchangeFeeLow)
    return revenue
 
# Takes the amount of coins, information about the high-price exchange, low-price exchange, and returns info about arbitrage opportunity.
def calculateProfitLoss(amount, high, low):
        
    # Fiat deposit fee in %.
    depositCost = float(100.00 - low.depositFee)/100.00
 
    # Exchange fee of lower currency in %.
    exchangeCostLow = float(100.00 - low.exchangeFee)/100.00
    # Exchange fee of higher currency in %.
    exchangeCostHigh = float(100.00 - high.exchangeFee)/100.00
   
    # Fiat withdrawal fee in %.
    withdrawCost = float(100.00 - high.withdrawFee)/100.00
  
    # Calculate revenue.
    # Original->  revenue = ((((amount * low.price) * depositCost)/low.price * exchangeCostLow) * high.price * exchangeCostHigh) * withdrawCost
    revenue = calcRev1(amount, low.price, high.price, exchangeCostLow, exchangeCostHigh, depositCost, withdrawCost)
    # revenue = calcRev2(amount, low.price, high.price, exchangeCostLow, exchangeCostHigh)
    
    # Profit/loss = revenue - investment.
    profit = revenue - (low.price * amount)
    # Round down to two decimals.
    profit = float('%.2f'%(profit))
    # Create opportunity object
    arbitrage = Opportunity()
    arbitrage.currency = high.currency
    arbitrage.buyExchange = low.name
    arbitrage.sellExchange = high.name
    arbitrage.profitLoss = profit
    arbitrage.sellPrice = '${:,.2f}'.format(high.price)
    arbitrage.buyPrice = '${:,.2f}'.format(low.price)
    arbitrage.amount = amount
    # Optimize by include exchange prices/fees?
    
    return arbitrage
###########################################################################

# Checks for an arbitrage opportunity for a given amount between exchanges.
def checkOpportunity(amount, gdax, gemini):
    
    # Set max opportunity amount to arbitrary negative number
    maxOpp = Opportunity()
    maxOpp.profitLoss = -999999999.99;
    
    # If GDAX price is higher.
    if gdax.price > gemini.price:
        # Calculate opportunities from 1 to amount.
        for i in range(1, amount):
            # Calculate profit/loss opportunity.
            opportunity = calculateProfitLoss(i, gdax, gemini)
            # If profit greater than the current max, update.
            if opportunity.profitLoss > maxOpp.profitLoss:
                maxOpp = opportunity
        return maxOpp
    # Else if Gemini price is higher.
    elif gdax.price < gemini.price:
        # Calculate opportunities from 1 to amount.
        for i in range(1, amount):
            # Calculate profit/loss opportunity.
            opportunity = calculateProfitLoss(i, gemini, gdax)
            # If profit greater than the current max, update.
            if opportunity.profitLoss > maxOpp.profitLoss:
                maxOpp = opportunity
        return maxOpp
    # Else prices equal, no arbitrage opportunity.
    elif gdax.price == gemini.price:
        return None
###################################################################

# Returns currency info at a given exchange.
def getExchange(xchg, curr):
    exchgInfo = Exchange()
    exchgInfo.name = xchg
    exchgInfo.currency = curr
    exchgInfo.price = getPrice(xchg, curr)
    exchgInfo.depositFee = getDepositFee(xchg, curr)
    exchgInfo.withdrawFee = getWithdrawFee(xchg, curr)
    exchgInfo.exchangeFee = getExchangeFee(xchg, curr)
    return exchgInfo
################################################################   

# Returns price of a currency at a given exchange.
def getPrice(xchg, curr):
    #price = 0.00
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
#######################################################

# Returns deposit % fee for a currency at a given exchange.
def getDepositFee(xchg, curr):
    
    fee = 0
    if xchg == 'gdax':
        if curr == 'BCH':
            fee = 0.00
        elif curr == 'ETH':
            fee = 0.001
        elif curr == 'LTC':
            fee = 0.00
        elif curr == 'BTC':
            fee = 0.001
    elif xchg == 'gemini':
        if curr == 'BTC':
            fee = 0.001
        elif curr == 'ETH':
            fee = 0.001
    return fee
###################################################

# Returns withdraw fee for a currency at a given exchange.
def getWithdrawFee(xchg, curr):
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
            #fee = 1.002
            fee = 0.00
        elif curr == 'ETH':
           # fee = 1.001
            fee = 0.00
    return fee

########################################################
# Returns exchange fee % for a given currency.
def getExchangeFee(exchange, curr):
    
    if exchange is "gdax":
        if curr == 'BCH':
            fee = 0.25
        elif curr == 'ETH':
            fee = 0.25
        elif curr == 'LTC':
            fee = 0.3
        elif curr == 'BTC':
            fee = 0.25
    elif exchange is "gemini":
            fee = 0.25
    return fee
########################################################