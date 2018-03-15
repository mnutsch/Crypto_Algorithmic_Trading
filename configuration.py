

# Set time interval(seconds) to check for opportunities.
INTERVAL = 60 # seconds

# Set phone numbers for text/sms notifications.
PHONE_NUMBERS = ['1234567890']
# Multiple phone numbers are possible.
# PHONE_NUMBERS = ['1234567890', '9876543210']
# Remove prior to submission.
# PHONE_NUMBERS = ['14696488502', '12539612914']
PHONE_NUMBERS = ['14696488502']

# Set email for email notifications.
EMAIL_LIST = ['sampleEmail@gmail.com']
# Multiple emails are possible.
#EMAIL_LIST = ['sampleEmail@gmail.com', 'sampleEmail2@gmail.com']
# Remove prior to submission.
EMAIL_LIST = ['timothy.bramlett@gmail.com']

# Set a threshold amount for opportunities you would 
# like to recieve notifications/execute trades on.
THRESHHOLD = 0
# Set maximum cost range of transactions (in dollars).  
# Application will search ranges from 0 to MAX_COST.
MAX_COST = 500
# Set the minimum profit range amount (in dollars) to return opportunities on.
# Note: losses are possible, to see negative profit/loss opportunities, 
# set MIN_PROFIT to a negative value.
MIN_PROFIT = 0
# Set true to send notifications via SMS.
NOTIFY_SMS = False
# Set true to send notifications via email.
NOTIFY_EMAIL = False
