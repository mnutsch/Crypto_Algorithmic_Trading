#!/usr/bin/python
import time
import readExchangeRatesGDAX
import readExchangeRatesGemini
import configuration
import sendSMS
import urllib

INTERVAL = 60 # seconds


PHONE_NUMBERS = ['14696488502', '12539612914']
THRESHHOLD = 500


def get_all_rates():
    """TODO: If we decide we need it"""
    pass


def main():


    while True:

        # Get the rates from all the exchanges
        print '\n\nCalling readExchangeRatesGemini()'
        print 'Calling readExchangeRatesGDAX'

        BTCToUSDFromGDAX = float(readExchangeRatesGDAX.getBTCToUSDFromGDAX())
        BTCToUSDFromGemini = float(readExchangeRatesGemini.getBTCToUSDFromGemini())

        
        print ''
        print 'BTCToUSDFromGDAX: {}'.format(BTCToUSDFromGDAX) 
        print 'BTCToUSDFromGemini: {}'.format(BTCToUSDFromGemini)
        

        # Analyze the rates to check for opportunities
        print '\nAnalyzing the rates...'
        diff = BTCToUSDFromGDAX - BTCToUSDFromGemini
        print 'Diff: {}'.format(abs(diff))

        # now lets check the abs diff between the two
        if abs(diff) >= THRESHHOLD:
            for phone in PHONE_NUMBERS:
                message = 'GDAX price: {} Gemini price: {}'.format(BTCToUSDFromGDAX, BTCToUSDFromGemini)
                message = urllib.quote_plus(message)
                print message
                sendSMS.sendSMSMessage(phone, message)

        # Wait for some specified interval
        # Repeat step one
        time.sleep(INTERVAL)



if __name__ == '__main__':
    main()


