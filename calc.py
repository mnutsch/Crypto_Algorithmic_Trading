# Name: calc.py
# Author: Patrick Mullaney
# Date Created: 2-8-2018
# Last Edited: 3-10-2018
# Description: This script checks contains calculation functions that can
# be used by checkSingleCurrencyOpps.py and checkMultipleCurrencyOpps.py.

import readExchangeRatesGDAX, readExchangeRatesGemini
import currency

# Number of pairwise comparisons = n(n-1)/2, for N = 12, comparisons = 66.

# Compares 3 currency conversion costs and returns true if there is a potentially profitable chain.  
# Example use: if ([BTC to ETH] > [ETH to LTC]) and ([LTC to BTC] < [ETH to LTC]), then buy ETH with BTC, buy LTC with ETH and buy BTC with LTC. 
def checkThree(cost1, cost2, cost3):
    if(cost1 > cost2) and (cost3 < cost2):
        return True
    else:
        return False
################################################################################

# Opportunity object stores the potential info about an exchange.
class Opportunity():
    buyCurrency = None
    sellCurrency = None
    buyExchange = None
    sellExchange = None
    buyPrice = None
    sellPrice = None
    amount = None
    profitLoss = 0.00
    
################################################################################

# Calculates revenue with deposit and withdraw fee costs.
def calcRev1(amount, lowPrice, highPrice, exchangeCostLow, exchangeCostHigh, depositCost, withdrawCost):
    revenue = ((amount * lowPrice) * depositCost)/lowPrice * exchangeCostLow * highPrice * exchangeCostHigh * withdrawCost
    return revenue
################################################################################

# Calculates revenue for multiple arbitrage opportunity (different currencies/exchanges possible).
def calcRev2(amount, sellPrice, buyPrice):
    amountToSell = amount/sellPrice
    sellValue = amountToSell * sellPrice
    amountToBuy = sellValue/buyPrice
    buyValue = amountToBuy * buyPrice
    revenue = buyValue - sellValue
    return revenue
 
 ################################################################################
 
# Takes the amount of coins, information about the high-price exchange, low-price exchange, and returns info about arbitrage opportunity.
def calculateProfitLoss(amount, high, low):
    #print "48 calc amt: {}, curr1: {}, curr2: {}".format(str(amount),str(high.name), str(low.name))
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
    #revenue = calcRev2(amount, low.price, high.price)
    
    # Profit/loss = revenue - investment.
    profit = revenue - (low.price * amount)
    # Round down to two decimals.
    profit = float('%.2f'%(profit))
    
    # Create opportunity object
    arbitrage = Opportunity()
    arbitrage.sellCurrency = high.name
    arbitrage.buyCurrency = low.name
    arbitrage.buyExchange = low.exchange
    arbitrage.sellExchange = high.exchange
    arbitrage.profitLoss = profit
    arbitrage.sellPrice = '${:,.2f}'.format(high.price)
    arbitrage.buyPrice = '${:,.2f}'.format(low.price)
    arbitrage.amount = amount
    
    return arbitrage
    
################################################################################

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
################################################################################

def multRevenue(curr1, curr2):
    revenue = 0.00
    depositCost = currency.getFeeCost(curr2, curr2.depositFee)
    revenue = ((curr2.amount * curr2.price) * depositCost)/curr2.price
    curr1XchgFee = currency.getFeeCost(curr1, curr1.exchangeFee)
    revenue = revenue * curr1XchgFee 
    revenue = revenue * curr1.price 
    curr2XchgFee = currency.getFeeCost(curr2, curr2.exchangeFee)
    revenue = revenue * curr2XchgFee
    withdrawCost = currency.getFeeCost(curr1, curr1.withdrawFee)
    revenue = revenue * withdrawCost
    return revenue
