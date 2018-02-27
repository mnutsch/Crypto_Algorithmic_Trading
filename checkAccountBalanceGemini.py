# Name: checkAccountBalanceGemini.py
# Author: Matt Nutsch
# Date Created: 2-12-2018
# Last Edited: 2-12-2018
# Description: This script reads the balance of an account from the exchange Gemini.

#DEV NOTE: CHANGE THESE TO READ FROM THE CONFIGURATION FILE
myAPIKey = "aaaaaaaaaa1aaaa1aaaa"
myAPISecret = "1aa11aaa1aaa1aaaaaaa1a11aaaa"
myNonce = 123473 #note: increase this value by 1 for each API call (by 2 if calling twice per run)

import hashlib
import requests
import base64
import hmac
from hashlib import sha384

###################################################

def getBTCAccountBalanceFromGemini(argAPIKey, argAPISecret, argNonce):

	url = "https://api.gemini.com/v1/balances"

	# for the purposes of this example, we've shown hand-rolled JSON - please import json and use json.dumps in your real code!
	b64 = base64.b64encode("""{
		"request": "/v1/balances",
		"nonce": """ + str(argNonce) + """
	}
	""")

	signature = hmac.new(argAPISecret, b64, hashlib.sha384).hexdigest()

	headers = {
		'Content-Type': "text/plain",
		'Content-Length': "0",
		'X-GEMINI-APIKEY': argAPIKey,
		'X-GEMINI-PAYLOAD': b64,
		'X-GEMINI-SIGNATURE': signature,
		'Cache-Control': "no-cache"
		}

	response = requests.request("POST", url, headers=headers)
	#print(response.text)

	#parse the JSON for only the account balance
	data = response.json()

	#output text to the user
	#print "The balance on the Gemini Bitcoin Core (BTC) account is: "
	#print data[0]["amount"] #BTC == 0, USD == 1, ETH == 2
	
	return data[0]["amount"];

###################################################

def getETHAccountBalanceFromGemini(argAPIKey, argAPISecret, argNonce):

	url = "https://api.gemini.com/v1/balances"

	# for the purposes of this example, we've shown hand-rolled JSON - please import json and use json.dumps in your real code!
	b64 = base64.b64encode("""{
		"request": "/v1/balances",
		"nonce": """ + str(argNonce) + """
	}
	""")

	signature = hmac.new(argAPISecret, b64, hashlib.sha384).hexdigest()

	headers = {
		'Content-Type': "text/plain",
		'Content-Length': "0",
		'X-GEMINI-APIKEY': argAPIKey,
		'X-GEMINI-PAYLOAD': b64,
		'X-GEMINI-SIGNATURE': signature,
		'Cache-Control': "no-cache"
		}

	response = requests.request("POST", url, headers=headers)
	#print(response.text)

	#parse the JSON for only the account balance
	data = response.json()

	#output text to the user
	#print "The balance on the Gemini Bitcoin Core (BTC) account is: "
	#print data[2]["amount"] #BTC == 0, USD == 1, ETH == 2
	
	return data[2]["amount"];

###################################################

print "Reading the balances of the Gemini accounts."
print "The balance on the Gemini Bitcoin Core (BTC) account is: " + getBTCAccountBalanceFromGemini(myAPIKey, myAPISecret, myNonce);
myNonce = int(myNonce) + 1;
print "The balance on the Gemini Ethereum (ETH) account is: " + getETHAccountBalanceFromGemini(myAPIKey, myAPISecret, myNonce);
