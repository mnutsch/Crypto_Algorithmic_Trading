##!/usr/bin/python
# Name: checkForMultipleCurrencyOpps.py
# Author: Patrick Mullaney
# Date Created: 2-8-2018
# Last Edited: 3-10-2018
# Description: This script checks for multiple currency arbitrage opportunities.

import readExchangeRatesGDAX, readExchangeRatesGemini
# Used in permutations.
import itertools
# Files used for calculations, currency info, and forming chain of transactions.
import calc, currency, conversions, chains

DEBUG = False

# From SO: Following two functions used for debugging.
# https://stackoverflow.com/questions/5969806/print-all-properties-of-a-python-class- used for debug    
def printTrans(trans):
    attrs = vars(trans)
    print ', '.join("%s: %s" % item for item in attrs.items())

def printChain(chain):
    for i in chain:
        printTrans(i)
        
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

def calcMultRev(curr1, curr2):
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
    
################################################################################

# Returns profit loss for a currency transaction for multiple arbitrage (potentially
# different exchanges, etc.).
def multProfitLoss(curr1, curr2, amount):
    #print "Starting profit/loss"
    #print "Curr 1: "
    #currency.printCurr(curr1)
    #print "Curr 2: "
    #currency.printCurr(curr2)
    profitLoss = 0
    # Amount of coins to sell.
    amountToSell = amount/curr1.price
    curr1.amount = amountToSell
    # Value of sale
    sellValue = amountToSell * curr1.price
    #print "amountToSell: {} (${})".format(str(amountToSell),str(sellValue))
    # Need fee cost of sale?
    # Amount of coins to buy.
    amountToBuy = sellValue/curr2.price
# added this here
    curr2.amount = amountToBuy
    buyValue = amountToBuy * curr2.price
    #print "amountToBuy: {} (${})".format(str(amountToSell), str(sellValue))
    revenue = buyValue - sellValue
    # modified from single:
    #depositCost = currency.getDepositCost(curr2)
    depositCost = currency.getFeeCost(curr2, curr2.depositFee)
    withdrawCost = currency.getFeeCost(curr1, curr1.withdrawFee)
    #curr1XchgFee = currency.getExchangeCost(curr1)
    curr1XchgFee = currency.getFeeCost(curr1, curr1.exchangeFee)
    curr2XchgFee = currency.getFeeCost(curr2, curr2.exchangeFee)
    # orig
    #revenue = ((amount * curr2.price) * depositCost)/curr2.price * curr1XchgFee * curr1.price * curr2XchgFee * withdrawCost
    # try 2   # should this be an amount to buy?
    revenue = ((curr2.amount * curr2.price) * depositCost)/curr2.price * curr1XchgFee * curr1.price * curr2XchgFee * withdrawCost
    #print "OG revenue: ", revenue
    revenue = calcMultRev(curr1, curr2)
    #print "New revenue: ", revenue
    # Profit/loss = revenue - investment.
    profitLoss = revenue - (curr1.price * curr1.amount)
    #profitLoss = revenue - (curr1.price * amount)
    '''
    print "Amount: ", amount
    print "withdraw % ", curr1.withdrawFee
    print "withdrawCost", withdrawCost
    print "depositCost: ", depositCost
    print "cur1 xchg fee: ", curr1XchgFee
    print "cur2 xchg fee: ", curr2XchgFee
    print "63 mult revenue:", revenue
    print "64 profitLoss: ", profitLoss
    print "Curr 1: "
    currency.printCurr(curr1)
    print "Curr 2: "
    currency.printCurr(curr2)'''
    return profitLoss

################################################################################

# Returns the calculated profit/loss for 3 currencies in a transaction chain.
def profitLoss3(curr1, curr2, curr3, amount):
    print "Starting profit/loss 3"
    profitLoss = 0.00
    print "Curr 1: "
    currency.printCurr(curr1)
    print "Curr 2: "
    currency.printCurr(curr2)
    # Amount of coins to sell.
    amountToSell = amount/curr1.price
    # Value of sale
    sellValue = amountToSell * curr1.price
    #print "amountToSell: {} (${})".format(str(amountToSell),str(sellValue))
    # Amount of coins to buy.
    curr2.amount = sellValue/curr2.price
    buyValue = curr2.amount * curr2.price
    #print "amountToBuy: {} (${})".format(str(curr2.amount), str(buyValue))
    # Revenue from first transaction.
    revenue = calcMultRev(curr1, curr2)
    # Profit/loss = revenue - investment of first transaction.
    firstProfitLoss = revenue - (curr1.price * curr1.amount)
    
    # Amount of coins to sell.
    amountToSell = amount/curr2.price
    # Value of sale
    sellValue = amountToSell * curr2.price
    #print "2. amountToSell: {} (${})".format(str(amountToSell),str(sellValue))
    # Amount of coins to buy.
    curr3.amount = sellValue/curr3.price
    buyValue = curr3.amount * curr3.price
    # Revenue from second transaction.
    revenue = calcMultRev(curr2, curr3)
    secondProfitLoss = revenue - (curr2.price * curr2.amount)
    profitLoss = firstProfitLoss + secondProfitLoss
    return profitLoss

################################################################################

# need to add gemini 
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

    if len(profitable) > 0:
        print "First profit: "
        chains.printChain(profitable[0])
        chains.chainProfitLoss(profitable[0])
    ''' # Alternative method for of calculating
    print "Testing profitLoss 3"
    profitLoss = profitLoss3(curr1, curr2, curr3, 10)
    print "profitLoss 3: ", profitLoss'''
    return profitable
    
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
    # Get list of permutations of all currency cost comparisons for chain up to three transactions.
    compPermutations = list(itertools.permutations(currencyPermutations, 3))
    # Get list of conversion costs.
    conversionCosts = conversions.getConversionList(amount, currencyList)
    #for i in conversionCosts:
    #   print "{}->{}: {}".format(str(i.curr1.name), i.curr2.name, str(i.cost))
    
    # Get list of positive conversion transactions.
    positiveConversions = conversions.getPositiveConversions(amount, currencyList)
    #print "0: ", positiveConversions[0]
    #print "Transaction: {}->{}: {}".format(str(positiveConversions[0][0].curr1.name), str(positiveConversions[0][0].curr2.name), str(positiveConversions[0][0].cost))
    # print positive conv 0
    #for i in positiveConversions[0]:
    #    print "Transaction: {}({})->{}({}): {}".format(str(i.curr1.name), str(i.curr1.exchange), str(i.curr2.name), str(i.curr2.exchange), str(i.cost))
    
    #print "Testing chain cost..."
    #chains.chainCost(positiveConversions[0])
    #print "Testing chain profit..."
    #chains.chainProfit(positiveConversions[0])
    
    # Get list of transaction chains up to 3 transactions.
    transactionChains = chains.getTransactionChains(currencyList)
    #print "transaction chain length: ", len(transactionChains)
    
    # Get list of profitable chains of transactions.
    profitable = getProfitableChains(transactionChains, amount)

    print "First profit: "
    chains.printChain(profitable[0])
    chains.chainProfitLoss(profitable[0])
    return profitable