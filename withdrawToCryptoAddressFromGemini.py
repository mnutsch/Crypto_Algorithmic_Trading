# Name: withdrawToCryptoAddressFromGemini.py
# Author: Matt Nutsch
# Date Created: 2-18-2018
# Last Edited: 3-5-2018
# Description: This script transfers crypto-currency from a Gemini address to an external address.
# Note: The external address has to be whitelisted in Gemini's account management console.

#DEV NOTE: CHANGE THESE TO READ FROM THE CONFIGURATION FILE
myAPIKey = "12345678asdbxcvasdCX"
myAPISecret = "12345457568asdasdfsdxv1231231"
myNonce = 234567 #note: increase the myNonce value by 1 for each API call

paymentAddress = "12345abcdef"
paymentAmount = 0

import hashlib
import requests
import base64
import hmac
from hashlib import sha384

###################################################

def transferBTCFundsFromGemini(argAPIKey, argAPISecret, argNonce, argAddress, argAmount):

	url = "https://api.sandbox.gemini.com/v1/withdraw/btc" #test API
	#url = "https://api.gemini.com/v1/withdraw/BTC" #production API, uncomment this for production use

	# for the purposes of this example, we've shown hand-rolled JSON - please import json and use json.dumps in your real code!
	b64 = base64.b64encode("""{
		"request": "/v1/withdraw/btc",
		"nonce": """ + str(argNonce) + """,
		"address": """ + str(argAddress) + """,
        "amount": """ + str(argAmount) + """
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
	#print "The JSON response is: "
	#print data
	
	if data["result"] == "error":
		return 0
	else:
		return 1
	

###################################################

###################################################

def transferETHFundsFromGemini(argAPIKey, argAPISecret, argNonce, argAddress, argAmount):

	url = "https://api.sandbox.gemini.com/v1/withdraw/eth" #test API
	#url = "https://api.gemini.com/v1/withdraw/eth" #production API, uncomment this for production use

	# for the purposes of this example, we've shown hand-rolled JSON - please import json and use json.dumps in your real code!
	b64 = base64.b64encode("""{
		"request": "/v1/withdraw/eth",
		"nonce": """ + str(argNonce) + """,
		"address": """ + str(argAddress) + """,
        "amount": """ + str(argAmount) + """
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
	#print "The JSON response is: "
	#print data
	
	if data["result"] == "error":
		return 0
	else:
		return 1
	

###################################################
	
print "Transfering funds from the Gemini BTC account."

if transferBTCFundsFromGemini(myAPIKey, myAPISecret, myNonce, paymentAddress, paymentAmount) == 1:
	print "Funds transferred successfully."
else:
	print "Failed to transfer the funds."

#myNonce = int(myNonce) + 1;
	
#if transferETHFundsFromGemini(myAPIKey, myAPISecret, myNonce, paymentAddress, paymentAmount) == 1:
#	print "Funds transferred successfully."
#else:
#	print "Failed to transfer the funds."


