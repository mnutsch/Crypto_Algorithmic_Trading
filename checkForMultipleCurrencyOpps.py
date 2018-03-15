##!/usr/bin/python
# Name: checkForMultipleCurrencyOpps.py
# Author: Patrick Mullaney
# Date Created: 2-8-2018
# Last Edited: 3-10-2018
# Description: This script checks for multiple currency arbitrage opportunities.

import readExchangeRatesGDAX, readExchangeRatesGemini
# Used in permutations and calculations.
import itertools, numpy
# Files used for calculations, currency info, and forming chain of transactions.
import calc, currency, conversions, chains
from configuration import OUTPUT

DEBUG = False

# From SO: Following two functions used for debugging.
# https://stackoverflow.com/questions/5969806/print-all-properties-of-a-python-class- used for debug    
def printTrans(trans):
    attrs = vars(trans)
    print ', '.join("%s: %s" % item for item in attrs.items())

def printChain(chain):
    for i in chain:
        printTrans(i)
        
# Opportunity object stores the potential info about a chain of transactions.
class multipleOpportunity():
    startingAmount = 0.00
    transactionChain = ""
    profitLoss = 0.00
        
################################################################################
'''
# Print cost for debugging.
def printCost(curr1, curr2):
    if DEBUG: 
        print "{} price: {}".format(curr1.name, str(curr1.price))
        print "{} amt: {}".format(curr1.name, str(curr1.amount))
        print "{} cost: {}".format(curr1.name, str(curr1.cost))
        print "{} price: {}".format(curr2.name,str(curr2.price))
        print "{} amt: {}".format(curr2.name,str(curr2.amount))
        print "{} cost: {}".format(curr2.name, str(curr2.cost))
    cost = curr1.cost + curr2.cost
    print "{}->{} cost: {}".format(curr1.name, curr2.name, str(cost))
'''
################################################################################
# Returns revenue for a transaction.
def calcMultRev(curr1, curr2):
    # Calculate revenue.
    revenue = 0.00
    # Get deposit cost.
    depositCost = currency.getFeeCost(curr2, curr2.depositFee)
    revenue = ((curr2.amount * curr2.price) * depositCost)/curr2.price
    # Get 1st currency exchange fee.
    curr1XchgFee = currency.getFeeCost(curr1, curr1.exchangeFee)
    revenue = revenue * curr1XchgFee 
    revenue = revenue * (curr1.price * curr1.amount)
    # Get 2nd currency exchange fee.
    curr2XchgFee = currency.getFeeCost(curr2, curr2.exchangeFee)
    revenue = revenue * curr2XchgFee
    # Factor in withdrawal costs.
    withdrawCost = currency.getFeeCost(curr1, curr1.withdrawFee)
    revenue = revenue * withdrawCost
    return revenue
  
################################################################################

# Returns profit loss for a currency transaction for multiple arbitrage (potentially
# different exchanges, etc.).
def multProfitLoss(curr1, curr2, amount):

    profitLoss = 0
    # Amount of coins to sell and value of sale.
    curr1.amount = amount/curr1.price
    sellValue = curr1.amount * curr1.price
    # Amount of coins to buy and value.
    curr2.amount = sellValue/curr2.price
    buyValue = curr2.amount * curr2.price
    revenue = buyValue - sellValue
    #revenue = ((curr2.amount * curr2.price) * depositCost)/curr2.price * curr1XchgFee * curr1.price * curr2XchgFee * withdrawCost
    #print "OG revenue: ", revenue
    revenue = calcMultRev(curr1, curr2)
    # Profit/loss = revenue - investment.
    #investment = (curr1.price * curr1.amount)
    #print "103 investment: ", investment # for debugging.
    profitLoss = revenue - (curr1.price * curr1.amount)
    return profitLoss

################################################################################

# Returns the calculated profit/loss for 3 currencies in a transaction chain
# (alternative method was explored to attempt to produce better results).
def profitLoss3(curr1, curr2, curr3, amount):
    profitLoss = 0.00
    # Amount of coins to sell and value of sale.
    amountToSell = amount/curr1.price
    sellValue = amountToSell * curr1.price
    # Amount of coins to buy and value of buy.
    curr2.amount = sellValue/curr2.price
    buyValue = curr2.amount * curr2.price
    # Revenue from first transaction.
    revenue = calcMultRev(curr1, curr2)
    # Profit/loss = revenue - investment of first transaction.
    firstProfitLoss = revenue - (curr1.price * curr1.amount)
    # Amount of coins to sell.
    amountToSell = amount/curr2.price
    # Value of sale
    sellValue = amountToSell * curr2.price
    # Amount of coins to buy.
    curr3.amount = sellValue/curr3.price
    buyValue = curr3.amount * curr3.price
    # Revenue from second transaction.
    revenue = calcMultRev(curr2, curr3)
    secondProfitLoss = revenue - (curr2.price * curr2.amount)
    profitLoss = firstProfitLoss + secondProfitLoss
    return profitLoss

################################################################################

# Returns list of arbitrage opportunties by focusing on transactions with most 
# profit (aggress approach, more profitable results).
def checkOpps(amount):
    # Get list of currencies.
    currencyList = currency.getCurrencyList()
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    possibleTransactions = len(currencyPermutations)
    print "Checking {} possible transactions...".format(str(possibleTransactions))
 
    # Get list of transaction chains up to 3 transactions.
    transactionChains = chains.getTransactionChains(currencyList)
    possibleChains = len(transactionChains)
    print "Checking {} possible transaction chains...".format(str(possibleChains))
    
    # Get list of profitable chains of transactions.
    profitable = getProfitableChains(transactionChains, amount)
    # If there are any opportunities, create list.
    opportunities = []
    if len(profitable) > 0:
        # Create opportunity object with relevant info for each profitable opportunity.
        for i in profitable:
            newOpp = multipleOpportunity()    
            newOpp.startingAmount = amount
            newOpp.profitLoss = chains.chainProfitLoss(i)
            newOpp.transactionChain = chains.chainMessage(i)
            opportunities.append(newOpp)
    ''' # Alternative method for of calculating
    print "Testing profitLoss 3"
    profitLoss = profitLoss3(curr1, curr2, curr3, 10)
    print "profitLoss 3: ", profitLoss'''
    #return profitable
    return opportunities
    
################################################################################

# Returns a list of profitable chain of transactions.
def getProfitableChains(transactionChains, amount):
    profitable = []
    # Iterate through chain of transactions.
    for chain in transactionChains:
        chainProfit = 0
        # Sum total profitLoss for chain.
        for transaction in chain:
            #printTrans(transaction)
            transaction.profitLoss = multProfitLoss(transaction.curr1,transaction.curr2, amount)
            chainProfit += transaction.profitLoss
        # If profitLoss for chain of transactions is profitable, add to list.
        if chainProfit > 0:
            profitable.append(chain)
    return profitable
    
################################################################################

# Returns list of arbitrage opportunties by focusing on lowest fees (conservative approach, did not have good results).
def checkOppsCost(amount):
    # Get list of currencies.
    currencyList = currency.getCurrencyList()
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    '''  Calculating by conversion costs was not as profitable.
    # Get list of conversion costs.
    conversionCosts = conversions.getConversionList(amount, currencyList)
    # Get list of positive conversion transactions.
    positiveConversions = conversions.getPositiveConversions(amount, currencyList)
    '''
    # Get list of transaction chains up to 3 transactions.
    transactionChains = chains.getTransactionChains(currencyList)
    #print "transaction chain length: ", len(transactionChains)
    
    # Get list of profitable chains of transactions.
    profitable = getProfitableChains(transactionChains, amount)
    return profitable

################################################################################
# Added new code below:

# Checks for multiple arbitrage opportunities, taking into consideration
# maximum cost and minimum profit.
def checkAllbyProfit(maxCost, minProfit):
    # Get list of currencies.
    currencyList = currency.getCurrencyList()
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    possibleTransactions = len(currencyPermutations)
    if OUTPUT:
        print "There are {} possible transactions...".format(str(possibleTransactions))
    # Get list of transaction chains up to 3 transactions.
    transactionChains = chains.getTransactionChains(currencyList)
    possibleChains = len(transactionChains)
    if OUTPUT:
        print "Checking {} possible transaction chains...".format(str(possibleChains))
    
    amount = maxCost
    # Get list of profitable transaction chains..
    profitable = getProfitableChainsByProfit(transactionChains, maxCost)
    opportunities = []
    # If there are any profitable transaction chains, return opportunities.
    if len(profitable) > 0:
        # Create opportunity object with relevant info for each profitable opportunity.
        for i in profitable:
            newOpp = multipleOpportunity()    
            # Add currencies, starting amt
            newOpp.startingAmount = amount
            newOpp.profitLoss = chains.chainProfitLoss(i)
            newOpp.transactionChain = chains.chainMessage(i)
            opportunities.append(newOpp)
    if OUTPUT is True and len(profitable) == 0:
        print "Currently no profitable multiple currency opportunities."
    # Return opportunities.
    return opportunities  
  
################################################################################

# Returns a list of profitable chain of transactions.
def getProfitableChainsByProfit(transactionChains, amount):
    # List of pofitable transaction chains.
    profitable = []
    # Iterate through chain of transactions.
    for chain in transactionChains:
        #chainProfit = 0
        # Changed this from .001 to .1 for performance reasons.
        oppList = numpy.arange(0.1, amount, 0.1)
        for i in oppList:
            chainProfit = 0
            maxProfitLoss = -999999999.99
            # Sum total profitLoss for chain.
            for transaction in chain:
                transaction.curr1.amount = (i/transaction.curr1.price)
                transaction.profitLoss = multProfitLoss2(transaction.curr1,transaction.curr2, transaction.curr1.amount)
                chainProfit += transaction.profitLoss
            # Update profitLoss if appropriate.
            if chainProfit > maxProfitLoss:
                maxProfitLoss = chainProfit
            # If profitLoss for chain of transactions is profitable, add to list.
            if chainProfit > 0: 
                profitable.append(chain)
    return profitable

################################################################################
# Returns profit loss for a currency transaction for multiple arbitrage 
#(potentially different exchanges, etc.).
def multProfitLoss2(curr1, curr2, amount):
    profitLoss = 0
    # Amount of coins to sell and value of sale.
    curr1.amount = amount/curr1.price
    sellValue = curr1.amount * curr1.price
    # Amount of coins to buy and value.
    curr2.amount = sellValue/curr2.price
    buyValue = curr2.amount * curr2.price
    revenue = buyValue - sellValue
    revenue = calcMultRev(curr1, curr2)
    # Profit/loss = revenue - investment.
    #investment = (curr1.price * curr1.amount) - used in debugging.
    profitLoss = revenue - (curr1.price * curr1.amount)
    return profitLoss

################################################################################
