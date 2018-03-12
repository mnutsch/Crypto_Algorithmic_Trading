#!/usr/bin/python
import time
import readExchangeRatesGDAX
import readExchangeRatesGemini
import configuration
import sendSMS
import urllib
import sendEmail
import os
import checkForSingleCurrencyOpps
import inspect
from pprint import pprint

INTERVAL = 60 # seconds
# PHONE_NUMBERS = ['14696488502', '12539612914']
PHONE_NUMBERS = ['14696488502']
THRESHHOLD = 0
EMAIL_LIST = ['timothy.bramlett@gmail.com', 'timbram@gmail.com']

# just for testing
sendEmail.sendSingleEmail('timothy.bramlett@gmail.com', 'main.py starting up...')


def notify_subscribed_via_email(message):
    for email in EMAIL_LIST:
        sendEmail.sendSingleEmail(email, message)

def notify_subscribed_via_sms(message):
    for phone in PHONE_NUMBERS:
        sendSMS.sendSMSMessage(phone, message)


def main():


    while True:

        result = checkForSingleCurrencyOpps.checkAllCurrencies(100)

        for opportunity in result:
            if opportunity.profitLoss < THRESHHOLD:
                message = """New Arbitrage opportunity: {}
                """.format(vars(opportunity))
                notify_subscribed_via_sms(message)
                notify_subscribed_via_email(message)

        # Wait for some specified interval
        # Repeat step one
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()


