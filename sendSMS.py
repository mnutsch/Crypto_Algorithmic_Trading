# Name: sendSMS.py
# Author: Matt Nutsch
# Date Created: 1-26-2018
# Last Edited: 1-27-2018
# Description: This script sends a SMS message through the service Tropo.

#example usage
#print "Sending SMS message."
#tropoNumberToDial = "15551112222"
#tropoMsg = "LoremIpsum"
#sendSMSMessage(tropoNumberToDial, tropoMsg);

import urllib, json, time
import os

#DEV NOTE: Replace these with values read from the configuration.py file.
tropoAPIToken = os.getenv('TROPO_API_TOKEN')
tropoSMSAuth = os.getenv('TROPO_SMS_AUTH')

def sendSMSMessage(phoneNumberToText, messageToSend):

	#DEV NOTE: url encode message
	#messageToSend = urllib.parse.quote_plus(messageToSend)

	url = "https://api.tropo.com/1.0/sessions?action=create&token=" + tropoAPIToken + "&numberToDial=" + phoneNumberToText + "&msg=" + messageToSend

	#read the page contents
	response = urllib.urlopen(url)

	#DEV NOTE: replace this with error detection
	#print "The Tropo response is: " + str(response)

	return;

