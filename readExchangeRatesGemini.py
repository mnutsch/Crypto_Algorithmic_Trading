# Name: readExchangeRatesGemini.py
# Author: Matt Nutsch
# Date: 1-19-2018
# Last Edited: 1-27-2018
# Description: This script reads cryptocurrency exchange rate information from the exchange Gemini.

#examples of calling the functions
#print "Reading the exchange rates from the Gemini exchange."
#print "The BTC-USD price is: " + getBTCToUSDFromGemini();
#print "The ETH-USD price is: " + getETHToUSDFromGemini();
#print "The ETH-BTC price is: " + getETHToBTCFromGemini();

#import libraries
import urllib, json, time

gemini_bchUsdPrice = 0.00
gemini_ethUsdPrice = 0.00
gemini_ethBtcPrice = 0.00

###################################################

def getBTCToUSDFromGemini():

	#BTC-USD
	#Get the BTC-USD price.

	#set up the URL
	url = "https://api.gemini.com/v1/pubticker/btcusd"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gemini_btcUsdPrice = data["ask"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The BTC-USD price is: " + gemini_btcUsdPrice

	#pause briefly
	time.sleep(.300)
	
	return gemini_btcUsdPrice;

###################################################

def getETHToUSDFromGemini():

	#ETH-USD
	#Get the ETH-USD price.

	#set up the URL
	url = "https://api.gemini.com/v1/pubticker/ethusd"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gemini_ethUsdPrice = data["ask"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The ETH-USD price is: " + gemini_ethUsdPrice

	#pause briefly
	time.sleep(.300)
	
	return gemini_ethUsdPrice;

###################################################

def getETHToBTCFromGemini():

	#ETH-BTC
	#Get the ETH-BTC price.

	#set up the URL
	url = "https://api.gemini.com/v1/pubticker/ethbtc"

	#read the page contents
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gemini_ethBtcPrice = data["ask"]

	#output the data so that we can see it
	#print "The raw output is: "
	#print data

	#print "The ETH-BTC price is: " + gemini_ethBtcPrice

	#pause briefly
	time.sleep(.300)
	
	return gemini_ethBtcPrice;
	
