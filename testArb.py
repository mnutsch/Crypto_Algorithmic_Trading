# Name: testArg.py
# Author: Patrick Mullaney
# Date Created: 2-10-2018
# Last Edited: 3-10-2018
# Description: This script runs on a console, checking for single currency 
# arbitrage opportunities with worst case scenario transaction fees.

import checkForSingleCurrencyOpps, sendEmail, exchange
import time

# Will genereate email if on: needs to be fixed.
emailNotice = False

# Print opportunity info
def printOpp(opp):
    print "Buy: {} @ {}: {}".format(opp.currency, opp.buyExchange, opp.buyPrice)
    print "Sell: {} @ {}: {}".format(opp.currency, opp.sellExchange, opp.sellPrice)
    print "Amount of coins: {}".format(opp.amount)
    print "Profit/Loss $: {}".format(opp.profitLoss)

print "****** Aribtage opportunities ******"

#amount = int(raw_input("Enter max amount of coins to buy/sell: "))
amount = 10
minProfitLoss = -5

print "Testing BTC & ETH..."

while True:
    print "Checking opps..."
     # Create gdax and gemini exchange objects for testing.
    gdaxBTC = exchange.getExchange1('gdax', 'BTC')
    gemBTC = exchange.getExchange1('gemini', 'BTC')
    # Check for opportunity.
    opp = checkForSingleCurrencyOpps.checkOpportunity(amount, gdaxBTC, gemBTC)
    if opp is not None:
        if opp.profitLoss > minProfitLoss:
            printOpp(opp)
            if emailNotice:
                sendEmail.sendSingleEmail4(opp)
    # Create gdax and gemini exchange objects for testing.
    gdaxETH = exchange.getExchange1('gdax', 'ETH')
    gemETH = exchange.getExchange1('gemini', 'ETH')
    # Check for opportunity.
    oppETH = checkForSingleCurrencyOpps.checkOpportunity(amount, gdaxETH, gemETH)
    if oppETH is not None:
        if oppETH.profitLoss > minProfitLoss:
            printOpp(oppETH)
            if emailNotice:
                sendEmail.sendSingleEmail4(oppETH)
    time.sleep(300)