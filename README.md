# Crypto_Algorithmic_Trading
This repository contains code for algorithmically trading cryptocurrencies.

<u><strong>Introduction:</strong></u>

This is a cryptocurrency app with the ability to perform algorithmic trading. Specifically, our app looks for arbitrage opportunities.

The app continuously queries the U.S. dollar exchanges rates of various cryptocurrencies. If it finds a situation where the exchange rates are not consistent, then it automatic executes a trade. In other words, this a bot which finds arbitrage opportunities for cryptocurrencies.

For example, the app will check the USD exchange rate for Bitcoin at the exchange GDAX and the exchange rate for Bitcoin at the exchange Gemini. If the associated fees are less than the difference in price, then the app will automatically execute a trade.

<strong>Team Members:</strong><br/>
<ul><li>Matt L. Nutsch - http://www.mattnutsch.com/</li>
<li>Patrick Mullaney - http://www.patricktmullaney.com/</li>
<li>Tim Bramlett - http://timothybramlett.com/</li></ul>

<strong>Documentation:</strong><br/>
"CRY0 - Original Project Plan.pdf" for the original project plan.<br/>
"CRY0 - Mid Point Project Check.pdf" for a mid point status update on the project.<br/>

Check out the video at this URL for a short video update on the mid point status of the project.
https://media.oregonstate.edu/media/t/1_0vcs7gjq

<hr>

<u><strong>Setup & Usage</strong></u>

<strong>Setup a web server</strong>
Set up a Linux web server. We recommend hosting the application on Amazon Web Services's (AWS) Elastic Cloud Compute (EC2) service. You can find instructions to do so here: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html

<strong>Download the project code</strong>
A repository on Github.com has been used to store the application's code. Navigate to the following URL and download the contents. Upload the extracted contents to the application web server. 
https://github.com/mnutsch/Crypto_Algorithmic_Trading

<strong>Install Python</strong>
Install Python on the web server. This application was built and tested with Python version 2.7.5. You can find instructions for installing the latest release of Python here: https://www.python.org/

<strong>Install Python libraries</strong>
From the Linux command prompt run the following command. It will install the libraries utilized by the application:
pip install -r requirements.txt

<strong>Set up Cryptocurrency exchange accounts</strong>
In order to transact in cryptocurrencies you will need to register accounts with the cryptocurrency exchanges that the application interfaces with. Note that it may take several days for the exchanges to process your account requests.
Create a user account at the GDAX exchange. Follow this URL for more information: https://www.gdax.com/
Create a user account at the Gemini exchange. Follow this URL for more information: https://gemini.com/
Add GDAX credentials to the file settings in the following files:
checkAccountBalanceGDAX.py
execTransactionsGDAX.py
withdrawToCryptoAddressGDAX.py
Add Gemini credentials to the file settings in the following files:
checkAccountBalanceGemini.py
execTransactionsGemini.py
withdrawToCryptoAddressGemini.py
Update the exchange fee amounts. 
Look up the latest fee amounts from the exchanges' websites.
Edit the following files and update the fee amounts to the latest numbers:
currency.py 
exchange.py

<strong>Set up a Tropo account for text (SMS) notifications</strong>
In order to receive notifications with text (SMS), you will need to register an account with Tropo. Note that it may take a couple of days for Tropo to process your account request once you register a payment method.
Create an account with the service Tropo. Follow this URL for more information: https://www.tropo.com/
Follow the instructions at this URL to install and configure the Tropo component of the application: https://github.com/mnutsch/Crypto_Algorithmic_Trading/blob/master/tropo/readme.txt
Edit the file configuration.py in a text editor. Input the phone number where you want to receive text (SMS) messages. You can enter one phone number in the format: 
PHONE_NUMBERS = ['15551234567'] 
Alternatively, you can enter multiple phone numbers in the format:
PHONE_NUMBERS = ['15551234567', '15551234568']
Edit the file .bashrc to include the API token and SMS authentication code for the Tropo app. The file .bashrc is a hidden file which resides in a Linux user's home directory. Add the following lines to the file. Update the values based on those of the app in Tropo.
export TROPO_API_TOKEN="12345abcdef"
export TROPO_SMS_AUTH="12345"
    
<strong>Set up an email account for email notifications</strong>
Register an account with an email service of your choice (i.e. Gmail).
If needed, enable third party email clients in the email service's settings.
Edit the file .bashrc to include the username and password for the email service. This is a hidden file which resides in a Linux user's home directory. Add the following lines to the file. Enter the email address and password for the email account where appropriate.
export GMAIL_EMAIL="yourEmail@gmail.com"
export GMAIL_PW="enterYourPasswordHere"
