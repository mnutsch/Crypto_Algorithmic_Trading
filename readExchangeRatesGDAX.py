# Name: readExchangeRatesGDAX.py
# Author: Matt Nutsch
# Date Created: 1-19-2018
# Last Edited: 1-27-2018
# Description: This script reads cryptocurrency exchange rate information from the exchange GDAX.

#examples of calling the functions
#print "Reading the exchange rates from the GDAX exchange."
#print "The BCH-USD price is: " + getBCHToUSDFromGDAX();
#print "The LTC-USD price is: " + getLTCToUSDFromGDAX();
#print "The BTC-USD price is: " + getBTCToUSDFromGDAX();
#print "The ETH-USD price is: " +  getETHToUSDFromGDAX();

#import libraries
import urllib, json, time

gdax_bchUsdPrice = 0.00
gdax_ethUsdPrice = 0.00
gdax_ltcUsdPrice = 0.00
gdax_btcUsdPrice = 0.00

###################################################

def getBCHToUSDFromGDAX():

	#BCH-USD
	#Get the BCH-USD price.

	#set up the URL
	url = "https://api.gdax.com/products/BCH-USD/ticker"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gdax_bchUsdPrice = data["price"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The BCH-USD price is: " + gdax_bchUsdPrice

	#pause briefly
	time.sleep(.300)
	
	return gdax_bchUsdPrice;

###################################################

def getETHToUSDFromGDAX():

	#ETH-USD
	#Get the ETH-USD price.

	#set up the URL
	url = "https://api.gdax.com/products/ETH-USD/ticker"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gdax_ethUsdPrice = data["price"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The ETH-USD price is: " + gdax_ethUsdPrice

	#pause briefly
	time.sleep(.300)
	
	return gdax_ethUsdPrice;

###################################################

def getLTCToUSDFromGDAX():

	#LTC-USD
	#Get the LTC-USD price.

	#set up the URL
	url = "https://api.gdax.com/products/LTC-USD/ticker"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gdax_ltcUsdPrice = data["price"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The LTC-USD price is: " + gdax_ltcUsdPrice

	#pause briefly
	time.sleep(.300)
	
	return gdax_ltcUsdPrice;

###################################################

def getBTCToUSDFromGDAX():

	#BTC-USD
	#Get the BTC-USD price.

	#set up the URL
	url = "https://api.gdax.com/products/BTC-USD/ticker"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gdax_btcUsdPrice = data["price"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The BTC-USD price is: " + gdax_btcUsdPrice

	#pause briefly
	time.sleep(.300)

	return gdax_btcUsdPrice;

###################################################
	




