# Name: chains.py
# Author: Patrick Mullaney
# Date Created: 3-3-2018
# Last Edited: 3-10-2018
# Description: This file contains functions related to obtaining a chain of valid transactions.

import calc, currency, conversions
import itertools

# Prints and returns a string for a chain of transactions. 
def printChain(chain):
    transactionChain = "Transaction chain: "
    for i in chain:
        transactionChain += str(i.curr1.name)
        transactionChain += str("(")
        transactionChain += str(i.curr1.exchange)
        transactionChain += str(")")
        transactionChain += str("->")
        transactionChain += str(i.curr2.name)
        transactionChain += str("(")
        transactionChain += str(i.curr2.exchange)
        transactionChain += str(")")
        transactionChain += str(". ")
    print transactionChain
    # Return string
    return transactionChain

################################################################################
    
# Returns list of all of possible transactions for all permutations.  
def getTransactionList(currencyList):
    # Get all permutations of currency list.
    currencyPermutations = list(itertools.permutations(currencyList, 2))
    # print "Currency permutations: ", len(currencyPermutations)
    # Get currencies for all transaction permutations.
    transactions = []
    for i in currencyPermutations:
        conv = conversions.Conversion()
        conv.curr1 = i[0]
        conv.curr2 = i[1]
        transactions.append(conv)
    #print "Transaction list length: {}".format(str(len(conversionCosts)))
    return transactions
    
################################################################################

# Returns a list of transaction chains up to 3 transactions each.
def getTransactionChains(currencyList):
    # Get list of transactions.
    transactions = getTransactionList(currencyList)
    # Get permutations of transactions.
    comparePermutations = list(itertools.permutations(transactions, 3))
    # Print size of list for testing.
    #print "48 Permutations: ", len(comparePermutations)
    # Get transaction chains.
    transactionChains = getChains(comparePermutations)
    return transactionChains

################################################################################

# Returns true if link2 is the potential next link in a chain of transactions,
# i.e. nextLink(BTC(gdax)->LTC(gemini), LTC(gemini)->BCH(gdax)) would return true.
def nextLink(link1, link2):
    if link1.curr2.name != link2.curr1.name:
        return False
    if link1.curr2.exchange != link2.curr1.exchange:
        return False
    if link1.curr1.name == link2.curr2.name and link1.curr1.exchange == link2.curr2.exchange:
        return False
    return True

################################################################################

# This function returns list of acceptable chain of transactions by ensuring
# all transactions are sequential, i.e. btc->eth transaction is only followed by 
# eth->[currency], eth->ltc transactions followed by ltc->[currency] etc.
def getChains(permutations):
    print "Permutations: ", len(permutations)
    chains = []
    # Iterate through permutations, if valid link, add to chain.
    for i in permutations:
        if nextLink(i[0], i[1]) and nextLink(i[1],i[2]):
            chains.append(i)
    return chains

################################################################################

# Returns the total cost of a chain of transactions.
def chainCost(chain):
    cost = 0.00
    for i in chain:
        cost += i.cost
    print "Total cost of chain of transactions: {}".format(str(cost))
    return cost

################################################################################

# Returns the total profit/loss of a chain of transactions.
def chainProfitLoss(chain):
    total = 0.00
    for i in chain:
        total += i.profitLoss
    print "Total profit/loss of transaction chain: {}".format(str(total))
    return total

################################################################################