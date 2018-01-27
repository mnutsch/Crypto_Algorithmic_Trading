# Name: sendSMS.py
# Author: Matt Nutsch
# Date Created: 1-26-2018
# Last Edited: 1-26-2018
# Description: This script sends a SMS message through the service Tropo.

import urllib, json, time

#DEV NOTE: Replace these with values read from the configuration.py file.
tropoAPIToken = "484e5954774f704c6751706e614d55694e6f4a7068487a74464369444b68686a5846684b4765684a48694853"
tropoSMSAuth = "13a5V1G7u"
tropoNumberToDial = "12539612914"
tropoMsg = "LoremIpsum"

#DEV NOTE: url encode message
#tropoMsg = urllib.parse.quote_plus(tropoMsg)

url = "https://api.tropo.com/1.0/sessions?action=create&token=" + tropoAPIToken + "&numberToDial=" + tropoNumberToDial + "&msg=" + tropoMsg

print "Sending SMS message."

#read the page contents
response = urllib.urlopen(url)

#DEV NOTE: replace this with error detection
print "The Tropo response is: " + str(response)


