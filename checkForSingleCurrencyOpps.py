##!/usr/bin/python
# Name: checkForSingleCurrencyOpps.py
# Author: Patrick Mullaney
# Date Created: 1-20-2018
# Last Edited: 3-10-2018
# Description: This script checks for single currency arbitrage opportunities.

import readExchangeRatesGDAX, readExchangeRatesGemini
import currency, exchange

# Opportunity object stores the potential info about an exchange.
class Opportunity():
    currency = None
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
    
# Calculates revenue without deposit and withdraw fee costs.
def calcRev2(amount, lowPrice, highPrice, exchangeFeeLow, exchangeFeeHigh):
    revenue = (amount * highPrice * exchangeFeeHigh) - (amount * lowPrice * exchangeFeeLow)
    return revenue
    
################################################################################

# Same results as calcRev1, just easier to read and prints out for debugging.
def calcRev3(amount, lowPrice, highPrice, exchangeFeeLow, exchangeFeeHigh, depositCost, withdrawCost):
    '''
    print "Amount: ", amount
    print "Low Price: ", lowPrice
    print "High Price: ", highPrice
    print "exchangeLow: ", exchangeFeeLow
    print "exchangeHigh: ", exchangeFeeHigh
    print "dep cost: ", depositCost
    print "withdrawCost: ", withdrawCost
    '''
    revenue = (amount * lowPrice) * depositCost
    revenue = revenue/lowPrice * exchangeFeeLow
    revenue = revenue * highPrice * exchangeFeeHigh
    revenue = revenue * withdrawCost
    return revenue

################################################################################

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

# Calculates arbitrage opportunities for all currencies at exchanges.
def checkAllCurrencies(amount):

    # amount = 100 - for testing.
    # GDAX ethereum (ETH) exchange info.
    gdaxEth = exchange.getExchange1('gdax', 'ETH')
    # Gemini ethereum (ETH) exchange info.
    geminiEth = exchange.getExchange1('gemini', 'ETH')
    # Check opportunities for ethereum.
    oppEth = checkOpportunity(amount, gdaxEth, geminiEth)
    
    # GDAX Bitcoin Core (BTC) exchange info.
    gdaxBtc = exchange.getExchange1('gdax', 'BTC')
    # Gemini Bitcoin Core (BTC) exchange info.
    geminiBtc = exchange.getExchange1('gemini', 'BTC')
    # Check opportunities for litecoin.
    oppBtc = checkOpportunity(amount, gdaxBtc, geminiBtc)
    
    # Return array of arbitrage opportunities.
    arbOpps = [oppEth, oppBtc]
    return arbOpps

################################################################################