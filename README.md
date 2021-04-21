# achievementcord
a bot that manages your custom game achievements

# Setup

First run this command `pip install -r requirements.tx`

This bot is very easy to setup, you just need to get a bot token, with all intents enabled.
Then run the **bot.py** file. 
If you have to change the IP from localhost to anything else you will find that inside of the **server.py** file.

# Function

Send bytes in **UTF8** via a socket to default: localhost:8765.
The format is **steam64id**,**achievment name**.
Make sure that you have added the achievement before with `a!add_achievement <achievment  name>`
