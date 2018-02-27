# Name: checkAccountBalanceGDAX.py
# Author: Matt Nutsch
# Date Created: 2-12-2018
# Last Edited: 2-12-2018
# Description: This script reads the balance of an account from the exchange GDAX.

# NOTE:
# Requires python-requests. Install with pip:
#   pip install requests
# or, with easy-install:
#   easy_install requests

#DEV NOTE: CHANGE THESE TO READ FROM THE CONFIGURATION FILE
myAPIKey = "1111a111aa11111aa1a1111111aa1a1a"
mySecretKey = "a1aaaaa1aaa1aaaaaaa1aaaaaaaaaa1aaaaaaaaa/aa1aaa1a1aaaaaaa+a1aaaaaaaaa1+aaaaaaaaaaaaaaa=="
myPassphrase = "aaaa1aa11aa1"
myBTCAccountID = "11a11a1a-a111-1111-1111-111111111111"
myETHAccountID = "11a11a1a-a111-1111-1111-111111111111"

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

###################################################

def getAccountBalanceFromGDAX(argAccountID):

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

	api_url = 'https://api.gdax.com/'
	auth = CoinbaseExchangeAuth(myAPIKey, mySecretKey, myPassphrase)

	# Get accounts
	r = requests.get(api_url + 'accounts/' + argAccountID, auth=auth)
	#print r.json()

	#parse the JSON for only the account balance
	data = r.json()

	#output text to the user
	#print "The balance on the GDAX Bitcoin Core (BTC) account is: "
	#print data["balance"]

	return data["balance"];

###################################################

#examples of calling the function
print "Reading the balances of the GDAX accounts."
print "The balance on the GDAX Bitcoin Core (BTC) account is: " + getAccountBalanceFromGDAX(myBTCAccountID);
#print "The balance on the GDAX Ethereum (ETH) account is: " + getAccountBalanceFromGDAX(myETHAccountID);