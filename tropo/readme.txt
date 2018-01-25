Instructions to set up a Tropo.com account.
Author: Matt Nutsch
Date: 1-24-2018

Introduction:
This application uses Tropo.com to send text (SMS) messages. To configure the application you will need to register an account with Tropo.

Navigate to this website in your browser: https://www.tropo.com/register
Complete the user registration web form and click Complete.
Tropo.com will send you an email with a confirmation link in it. Click on that link to confirm your user account.
Log in to Tropo using the username and password that you entered during registration.
Check the circle next to Scripting API.
Click Create New App.
Click New Script.
Select Python under Editor.
Type the following in the Filename field: "tropoSendSMS.py"
Click Save
Name the new app "algorithmicTradingAlerts".
Choose United States under Country.
Under Phone number, choose "Standard: Voice and SMS" and a city near you.
Click Create App.
To the right of Text Script, click Edit script.
Copy the contents of "tropoSendSMS.py" from the Github repo and paste it into the Tropo app.
Click save.

Before your Tropo account can send SMS messages, you have to contact Tropo Support and ask them to enable outbound SMS messages.
Do this by e-mailing Tropo Support at support@tropo.com requesting that they do so. Be sure to give them your Tropo username.

When you are ready to use the application as a production level application, you will also need to upgrade the account with a payment method.
Do this by navigating to https://www.tropo.com/billing/upgrade and entering your credit card information.

Finally, you need to tell the algorithmic trading application how to call Tropo. 
Go to this link to get a list of your Tropo applications: https://www.tropo.com/applications
Click on the algorithmicTradingAlerts application.
Click on API Keys to the left.
Copy the key under "Messaging".
Edit the "configuration.py" file in the algorithmic trading app and enter the Tropo API Key in the appropriate field. 




