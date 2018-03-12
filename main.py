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
import execTransactionsGemini
import execTransactionsGDAX


# just for testing
# sendEmail.sendSingleEmail('timothy.bramlett@gmail.com', 'main.py starting up...')


def notify_subscribed_via_email(opp, message):
    for email in EMAIL_LIST:
        sendEmail.sendSingleEmail(email, message)
        # sendEmail.sendSingleEmailTemplate(opp)

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
                notify_subscribed_via_email(opportunity, message)

        # Wait for some specified interval
        # Repeat step one
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()


