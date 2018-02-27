# Name: withdrawToCryptoAddressFromGDAX.py
# Author: Matt Nutsch
# Date Created: 2-18-2018
# Last Edited: 2-26-2018
# Description: This script transfers crypto-currency from a GDAX address to an external address.

# NOTE:
# Requires python-requests. Install with pip:
#   pip install requests
# or, with easy-install:
#   easy_install requests

# Note:
# Use the tool at this URL to get your Gemini deposit address
# https://exchange.gemini.com/deposit/btc

#DEV NOTE: CHANGE THESE TO READ FROM THE CONFIGURATION FILE
myAPIKey = "1111111111111111111111111111"
mySecretKey = "111111111111111111111111111111111111111111111111111111111111111111111"
myPassphrase = "111111111111"
myBTCAccountID = "11a11a1a-a111-1111-1111-111111111111"
myETHAccountID = "11a11a1a-a111-1111-1111-111111111111"

myGeminiBTCDepositAddress = "1ECY1hFsSjBTbFvLQvtvTme37WpaxyxPy5"
myGeminiETHDepositAddress = "0x31bAB7D927B986aF4c2dBAaB536F7eEc6e469c93"

apiCallStatus = 0;

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

###################################################

def transferFundsFromGDAX(argAmount, argCurrency, argCryptoAddress):

	#set the variable which will hold the return value
	apiCallStatus = 0;

	# Create custom authentication for Exchange
	class CoinbaseExchangeAuth(AuthBase):
		def __init__(self, api_key, secret_key, passphrase):
			self.api_key = myAPIKey
			self.secret_key = mySecretKey
			self.passphrase = myPassphrase

		def __call__(self, request):
			timestamp = str(time.time())
			message = timestamp + request.method + request.path_url + (request.body or '')
			hmac_key = base64.b64decode(self.secret_key)
			signature = hmac.new(hmac_key, message, hashlib.sha256)
			signature_b64 = signature.digest().encode('base64').rstrip('\n')

			request.headers.update({
				'CB-ACCESS-SIGN': signature_b64,
				'CB-ACCESS-TIMESTAMP': timestamp,
				'CB-ACCESS-KEY': self.api_key,
				'CB-ACCESS-PASSPHRASE': self.passphrase,
				'Content-Type': 'application/json'
			})
			return request

	api_url = 'https://api.gdax.com/' #live #uncomment this and comment out the following line to 
	#api_url = 'https://public.sandbox.gdax.com/' #sandbox #uncomment this to test the API
	
	auth = CoinbaseExchangeAuth(myAPIKey, mySecretKey, myPassphrase)

	# Get accounts
	r = requests.get(api_url + 'withdrawals/crypto', auth=auth)
	#print "r == " + vars(r)

	#parse the JSON for only the transfer status
	#check status here

	if r.status_code == 200:
		apiCallStatus = 1
	else:
		apiCallStatus = 0

	return apiCallStatus;

###################################################

#example of calling the function
#print "Transfering funds from the GDAX BTC account."
#if transferFundsFromGDAX(0, "BTC", myGeminiBTCDepositAddress) == 1:
#	print "Funds transferred successfully."
#else:
#	print "Failed to transfer the funds."