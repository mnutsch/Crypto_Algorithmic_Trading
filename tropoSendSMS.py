# Name: tropoSendSMS.py
# Author: Matt Nutsch
# Date Created: 1-26-2018
# Last Edited: 1-26-2018
# Description: This script sends a SMS message through the service Tropo.

call("+" + numberToDial, {
    "network":"SMS"})
say(msg)
log("Sent the following message to " + numberToDial + ": " + msg)