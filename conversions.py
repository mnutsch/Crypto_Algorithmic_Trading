# Name: conversion.py
# Author: Patrick Mullaney
# Date Created: 3-1-2018
# Last Edited: 3-10-2018
# Description: This file contains functions related to obtaining conversion costs, return a list of conversions, etc.

import itertools
import currency, chains, calc

# Object containing cost information of conversion of purchasing currency 2 to currency 1.
class Conversion():
        curr1 = ""
        curr2 = ""
        cost = 0.00
        profitLoss = 0.00

################################################################################

# Dynamic Programming implentation of get conversion costs.
def getConversionCost(convTable, amount, curr1, curr2):
    
    if curr1.name == 'BTC' and curr1.exchange == 'gdax':
        row = 0
        col = 0
    elif curr1.name == 'BCH':
        row = 1
    elif curr1.name == 'ETH' and curr1.exchange == 'gdax':
        row = 2
    elif curr1.name == 'LTC':
        row = 3
    elif curr1.name == 'BTC' and curr1.exchange == 'gemini':
        row = 4
    elif curr1.name == 'ETH' and curr1.exchange == 'gemini':
        row = 5
    
    if curr2.name == 'BTC' and curr2.exchange == 'gdax':
        col = 0
    elif curr2.name == 'BCH':
        col = 1
    elif curr2.name == 'ETH' and curr2.exchange == 'gdax':
        col = 2
    elif curr2.name == 'LTC':
        col = 3
    elif curr2.name == 'BTC' and curr2.exchange == 'gemini':
        col = 4
    elif curr2.name == 'ETH' and curr2.exchange == 'gemini':
        col = 5

    # If conversion cost has been calculated, get cost, else calculate it.
    if convTable[row][col] != -999999999:
        cost = convTable[row][col]
    else:
        curr1.amount = amount/curr1.price
        curr1.cost = currency.getCost(curr1, curr1.amount)
        #gdax_btcCost = btcAmt * gdax_btcCost
        curr2.amount = amount/curr2.price
        curr2.cost = currency.getCost(curr2, curr2.amount)
        #gdax_ethCost = ethAmt * gdax_ethCost
        cost = curr1.cost + curr2.cost
        # Update table with calculated cost.
        convTable[row][col] = cost
    #printCost(curr1, curr2)
    return cost

################################################################################

''' Referenced this for guide to 2D array in python: 
https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array-in-python '''
# Builds a 2D table for dynamic programming implementation of conversion list.
def getConvTable():
    # Table is currently 6 x 6.
    col, row = 6, 6
    # Initialize all values to arbitrary large negative number.
    convTable = [[-999999999 for c in range(col)] for r in range(row)]
    return convTable

################################################################################

# Estimated cost of buying $x amount of currency 2 with $x amount of currency 1.
def getConversionCostOG(amount, curr1, curr2):
    curr1.amount = amount/curr1.price
    curr1.cost = currency.getCost(curr1, curr1.amount)
    #gdax_btcCost = btcAmt * gdax_btcCost
    curr2.amount = amount/curr2.price
    curr2.cost = currency.getCost(curr2, curr2.amount)
    #gdax_ethCost = ethAmt * gdax_ethCost
    cost = curr1.cost + curr2.cost
    #printCost(curr1, curr2)
    return cost

################################################################################

''' Reviewed permutation calculations at wikipedia to calculate for correctness.
# of permutations should be equal to n!/(n-k)! where n is number of elements and k
is the number we are selecting.  K will always be 2 as we are calculating pairs.
https://en.wikipedia.org/wiki/Permutation'''
# (DP implementation) Returns list of all permutations of conversion costs between two currencies.  
def getConversionList(amount, currencyList):
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    # print "Currency permutations: ", len(currencyPermutations)
    convTable = getConvTable()
    # Get conversion cost for all permutations.
    conversionCosts = []
    for i in currencyPermutations:
        conv = Conversion()
        conv.curr1 = i[0]
        conv.curr2 = i[1]
        conv.cost = getConversionCost(convTable, amount, i[0],i[1])
        #conv.profit = getConversionProfit(amount, i[0], i[1])
        conversionCosts.append(conv)
    #print "Conversion length: {}".format(str(len(conversionCosts)))
    return conversionCosts

################################################################################

# Returns list of all permutations of conversion costs between two currencies.  
def getConversionListOG(amount, currencyList):
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    # print "Currency permutations: ", len(currencyPermutations)
    # Get conversion cost for all permutations.
    conversionCosts = []
    for i in currencyPermutations:
        conv = Conversion()
        conv.curr1 = i[0]
        conv.curr2 = i[1]
        conv.cost = getConversionCostOG(amount, i[0],i[1])
        #conv.profit = getConversionProfit(amount, i[0], i[1])
        conversionCosts.append(conv)
    #print "Conversion length: {}".format(str(len(conversionCosts)))
    return conversionCosts

################################################################################

# Iterates through all permutations of conversion transaction costs and returns a list of potentially profitable ones.
def getPositiveConversions(amount, currencyList):
    conversionCosts = getConversionList(amount, currencyList)
    comparePermutations = list(itertools.permutations(conversionCosts, 3))
    # Print size of list for testing.
    #print "129 Permutations: ", len(comparePermutations)
    # Get transaction chains.
    transactionChains = chains.getChains(comparePermutations)
    
    # Get list of profitable 3-transaction changes.
    positiveConversions = []
    #for i in comparePermutations:
    for i in transactionChains:
        # Check if cost of (transaction 1 > transaction 2) and (transaction 3 < transaction 2)
        result = calc.checkThree(i[0],i[1],i[2])
        if result is True:
            positiveConversions.append(i)
            #print i.curr1.name, i.curr2.name, i.cost
    # Print size of list for testing.
    #print "Positive conversions: {}".format(str(len(positiveConversions)))
    #for i in positiveConversions:
    #  for x in i:
    #     print "{}({})->{}({})".format(str(x.curr1.name), str(x.curr1.exchange),str(x.curr2.name), str(x.curr2.exchange))
    return positiveConversions