# Name: checkForMultipleCurrencyOpps.py
# Author: Patrick Mullaney
# Date Created: 2-8-2018
# Last Edited: 2-17-2018
# Description: This script checks for multiple currency arbitrage opportunities.

#### Review: GEMINI does not support LTC/BCH

import readExchangeRatesGDAX, readExchangeRatesGemini
# Used in permutations
import itertools
# file used for calculations
import calc 

DEBUG = False
    
#Returns the estimated cost from buying an amount of currency at a given exchange. 
'''def getCost(amount, currency, exchange):
    cost = 0.00
    cost = amount * getPrice(exchange, currency)
    cost = cost + getWithdrawFee(currency, exchange)
    return cost'''
# Object containing information about a currency.
class Currency():
    name = None,
    amount = 0.00,
    cost = 0.00,
    price = 0.00

# Object containing cost information of conversion of purchasing currency 2 to currency 1.
class Conversion():
        curr1 = ""
        curr2 = ""
        cost = 0.00
    
# Returns value ratue of currency1:currency2 (helpful for testing).
def getRatio(curr1, curr2):
    curr1.cost = getCost(curr1, 1)
    curr2.cost = getCost(curr2, 1)
    ratio = curr1.cost/curr2.cost
    print "{}->{} ratio: {}".format(curr1.name, curr2.name, str(ratio))    
    return ratio

# Returns a currency object with name and price initialized - add fees?
def getCurrency(name):
    curr = Currency()
    curr.name = name
    curr.price = calc.getPrice('gdax', curr.name)
    return curr

# Need to add more fees?
def getCost(curr, amount):
    if curr.name == 'BTC' or curr.name == 'BCH':
        fee = 0.25
    elif curr.name == 'ETH' or curr.name == 'LTC':
        fee = 0.3
    currFee = (amount * curr.price * fee)/100.00
    cost = (amount * curr.price) + currFee
    return cost
    
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

# Estimated cost of buying $x amount of currency 2 with $x amount of currency 1.
def getConversionCost(amount, curr1, curr2):
    curr1.amount = amount/curr1.price
    curr1.cost = getCost(curr1, curr1.amount)
    #gdax_btcCost = btcAmt * gdax_btcCost
    curr2.amount = amount/curr2.price
    curr2.cost = getCost(curr2, curr2.amount)
    #gdax_ethCost = ethAmt * gdax_ethCost
    cost = curr1.cost + curr2.cost
    printCost(curr1, curr2)
    return cost

# Returns list of currency objects.
def getCurrencyList():
    btc = getCurrency('BTC')
    eth = getCurrency('ETH')
    ltc = getCurrency('LTC')
    bch = getCurrency('BCH')
    currencyList = [btc, eth, ltc, bch]
    return currencyList

# Returns list of all permutations of conversion costs between two currencies.  
def getConversionList(amount):
    ''' Reviewed permutation calculations at wikipedia to calculate for correctness.
    # of permutations should be equal to n!/(n-k)! where n is number of elements and k
    is the number we are selecting.  K will always be 2 as we are calculating pairs.
    https://en.wikipedia.org/wiki/Permutation'''
    # Get all permutations of currency list.
    currencyList = getCurrencyList()
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    # print "Currency permutations: ", len(currencyPermutations)
    
    # Get conversion cost for all permutations.
    conversionCosts = []
    for i in currencyPermutations:
        conv = Conversion()
        conv.curr1 = i[0]
        conv.curr2 = i[1]
        conv.cost = getConversionCost(amount, i[0],i[1])
        conversionCosts.append(conv)
    #print "Conversion length: {}".format(str(len(conversionCosts)))
    return conversionCosts

# if ([BTC to ETH] > [ETH to LTC]) and ([LTC to BTC] < [ETH to LTC]) 
# then buy ETH with BTC, buy LTC with ETH and buy BTC with LTC.    

# Iterates through all permutations of conversion transaction costs and returns a list of potentially profitable ones.
def getPositiveConversions():
    conversionCosts = getConversionList(100.00)
    comparePermutations = list(itertools.permutations(conversionCosts, 3))
    # Print size of list for testing.
    print len(compPerm)
    # Get list of profitable 3-transaction changes.
    positiveConversions = []
    for i in comparePermutations:
        # Check if cost of (transaction 1 > transaction 2) and (transaction 3 < transaction 2)
        result = calc.checkThree(i[0],i[1],i[2])
        if result is True:
            positiveConversions.append(i)
        #print i.curr1.name, i.curr2.name, i.cost
    # Print size of list for testing.
    print "Positive conversions: {}".format(str(len(positiveConversions)))
    return positiveConversions



# need to add gemini and finish this 
def checkOpps():
    amount = 100.00
    