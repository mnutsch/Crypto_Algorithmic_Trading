#!/usr/bin/python

# Name: logCryptoPrices.py
# Author: Matt Nutsch
# Date: 2-1-2018
# Last Edited: 2-5-2018
# Description: This script checks cryptocurrency prices and writes them to a log.

import readExchangeRatesGDAX
import readExchangeRatesGemini

import datetime
import time

filename = "priceLogs.csv"
textToWrite = ""

print ("This script will check the exchange rates of currencies and then log them in the file" + filename)

#read the currency prices from APIs
	
print "Reading the exchange rates from the GDAX exchange."
GDAXBCHUSD = readExchangeRatesGDAX.getBCHToUSDFromGDAX();
GDAXLTCUSD = readExchangeRatesGDAX.getLTCToUSDFromGDAX();
GDAXBTCUSD = readExchangeRatesGDAX.getBTCToUSDFromGDAX();
GDAXETHUSD = readExchangeRatesGDAX.getETHToUSDFromGDAX();

print "Reading the exchange rates from the Gemini exchange."
GEMBTCUSD = readExchangeRatesGemini.getBTCToUSDFromGemini();
GEMETHUSD = readExchangeRatesGemini.getETHToUSDFromGemini();

print "The BCH-USD price is: " + GDAXBCHUSD
print "The LTC-USD price is: " + GDAXLTCUSD
print "The BTC-USD price is: " + GDAXBTCUSD
print "The ETH-USD price is: " +  GDAXETHUSD

print "The BTC-USD price is: " + GEMBTCUSD
print "The ETH-USD price is: " + GEMETHUSD

#save the currency prices to the file

print ("Writing to the file: " + filename)

textToWrite = str(datetime.datetime.now()) + "," + str(GDAXBCHUSD) + "," + str(GDAXLTCUSD) + "," + str(GDAXBTCUSD) + "," + str(GDAXETHUSD) + "," + str(GEMBTCUSD) + "," + str(GEMETHUSD)

with open(filename, 'a') as f:
	f.write(textToWrite +  '\n')

