# Name: sendEmail.py
# Author: Patrick Mullaney
# Date Created: 1-28-2018
# Last Edited: 3-11-2018
# Description: This script sends emails notifying of potential arbitrage opportunities.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Message headers
# fromaddr = "[sending email]"
toaddr = "[receiving email]"
fromaddr = os.getenv('GMAIL_EMAIL')
password = os.getenv('GMAIL_PW')
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "CryO Opportunity"

addressToSend = "[receiving email]"
# fromaddr = os.getenv('GMAIL_EMAIL')
# password = os.getenv('GMAIL_PW')

################################################################################

# Initiate server.
def initServer(fromaddr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)  # change to osu? port?
    server.ehlo() # or .helo() for non ESMTP server?
    server.starttls()
    server.ehlo() # or .helo() for non ESMTP server?
    server.login(fromaddr, password)
    return server

################################################################################

# Set message headers
def setHeader(fromaddr, toaddr):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "CryO Opportunity"
	return msg

################################################################################
# Init Server
server = initServer(fromaddr, password)

################################################################################

# Sends a notification email for multiple arbitrage opportunities.
def sendMultipleEmail(addressToEmail, messageToSend):
    body = messageToSend
    #body = "Testing multiple currency email"
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, addressToEmail, text)

################################################################################

# Send notification that includes the currency, each exchange rate pricing, fee pricing, and the estimated profit. 
def sendSingleEmail(addressToEmail, messageToSend):
    # body = "Testing single currency email"
    body = messageToSend
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, addressToEmail, text)

################################################################################
# Send email notification of exchange rate pricing and estimated profit.
def sendSingleEmailTemplate(opp):
    # Convert output to dollars + cents
    profitLoss = '${:,.2f}'.format(opp.profitLoss)
    body = "Arbitrage Opportunity:\n\nCurrency: "
    body += opp.currency + "\n"
    body += "Buy: {} @ {}: {}\n".format(opp.currency, opp.buyExchange, opp.buyPrice)
    body += "Sell: {} @ {}: {}\n".format(opp.currency, opp.sellExchange, opp.sellPrice)
    body += "Amount of coins: {}\n".format(opp.amount)
    body += "Profit/Loss: {}\n".format(opp.profitLoss)
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    
################################################################################
    
# Returns a message template for multiple arbitrage opportunities.
def multipleEmailTemplate(opps):
    
    body = "Multiple Arbitrage Opportunities:\n\n"
    for i in opps:
        body += "Starting amount: {}\n".format(i.startingAmount)
        body += "{}\n".format(i.transactionChain)
        # Convert output to dollars + cents
        profitLoss = '${:,.2f}'.format(i.profitLoss)
        body += "Profit/Loss: {}\n\n".format(profitLoss)
    return body