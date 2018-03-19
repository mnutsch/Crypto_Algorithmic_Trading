#!/usr/bin/python
import time
import readExchangeRatesGDAX
import readExchangeRatesGemini
from configuration import *
import sendSMS
import urllib
import sendEmail
import os
import checkForSingleCurrencyOpps
import checkForMultipleCurrencyOpps
import execTransactionsGemini
import execTransactionsGDAX


# just for testing
# sendEmail.sendSingleEmail('myEmail@gmail.com', 'main.py starting up...')


def notify_subscribed_via_email(opp, message):
    for email in EMAIL_LIST:
        sendEmail.sendSingleEmail(email, message)
        # sendEmail.sendSingleEmailTemplate(opp)

def notify_subscribed_via_sms(message):
    for phone in PHONE_NUMBERS:
        sendSMS.sendSMSMessage(phone, message)


def main():

    while True:

        print "\nChecking single currency arbitrage opportunities..."
        #result = checkForSingleCurrencyOpps.checkAllCurrencies(100)
        result = checkForSingleCurrencyOpps.checkAllbyProfit(MAX_COST, MIN_PROFIT)
        # If no results, log to console, else handle results.
        if len(result) is 0:
            print "Currently no profitable single currency opportunities."
        else:
            for opportunity in result:
                # for testing
                #print "Profit/loss: ", opportunity.profitLoss
                #if opportunity.profitLoss < THRESHHOLD:
                if opportunity.profitLoss > THRESHHOLD:
                    message = """New Arbitrage opportunity: {}
                    """.format(vars(opportunity))
                    # Print message to console.
                    print (message)
                    # Send notifications if selected.
                    if NOTIFY_SMS:
                        notify_subscribed_via_sms(message)
                    if NOTIFY_EMAIL:
                        notify_subscribed_via_email(opportunity, message)
                    
            
        # Check for multiple opportunities.
        print "\nChecking multiple currency arbitrage opportunities..."
        multResult = checkForMultipleCurrencyOpps.checkAllbyProfit(MAX_COST, MIN_PROFIT)
        # Handle results if there are any.
        if len(multResult) > 0:
            for opportunity in multResult:
                # for testing
                print "Profit/loss: ", opportunity.profitLoss
                #if opportunity.profitLoss < THRESHHOLD:
                if opportunity.profitLoss > THRESHHOLD:
                    message = """New Arbitrage opportunity: {}
                    """.format(vars(opportunity))
                    # Print message to console.
                    print (message)
                    # Send notifications if selected.
                    if NOTIFY_SMS:
                        notify_subscribed_via_sms(message)
                    if NOTIFY_EMAIL:
                        notify_subscribed_via_email(opportunity, message)
                
        # Wait for some specified interval
        # Repeat step one
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()


