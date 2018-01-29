#!/usr/bin/python
import time
import readExchangeRatesGDAX
import readExchangeRatesGemini
import configuration

INTERVAL = 60 # seconds



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
        print 'Diff: {}'.format(diff)

        # now lets check the abs diff between the two
        if abs(diff) >= 50.0:
            print '\t!!!! HELLO OPPORTUNITY WORLD!!!!!'


        # Notify if opportunities exist
        print '\nIf opportunities exist...'
        print 'I will call sendSMS()'

        # Wait for some specified interval
        # Repeat step one
        time.sleep(INTERVAL)



if __name__ == '__main__':
    main()


