This directory contains a Python script which will read and document cryptocurrency prices every hour. 

Instructions:
Log into the linux server using SSH (i.e. PuTTY)
Navigate to the directory with the app.
Type "npm install forever". This will install forever.js.
Type "./node_modules/forever/bin/forever start -c python /nfs/stak/users/nutschm/CS467/logCryptoPrices.py". This will run the script endlessly.
Historical currency prices will be appended to the file "priceLogs.csv".

Notes:
The python script needs to have an infinite loop in it.
The command "./node_modules/forever/bin/forever list" will list the running processes.
The command "./node_modules/forever/bin/forever stopall" will stop all running processes.
