# REDDIT DISCORD BOT

Discord Bot that sends reddit posts on request with the help of [discord API](https://discordpy.readthedocs.io/) and [Reddit API](https://praw.readthedocs.io/).


## COMMANDS 

    !send [category] [subreddit]
    category = top/new/rising/hot/controversial
    subreddit = subreddit's name

    eg. !send top learnprogramming

## SETTING UP THE BOT

We need to have all the requirements first.

1. Install Python from https://www.python.org/ 

2. Installing the dependencies :
    ```bash
    sudo python3 -m pip install --upgrade -r requirements.txt
    ```

3. Clone this repository to your computer by typing the command : 
   
   ```bash
    git clone https://github.com/harsh23exe/Reddit-Disord-Bot.git
    ```

### LINK DISCORD BOT 

Go to https://discordapp.com/developers/applications/me and click the app that represents your Bot. Under the Bot paragraph you should see Token: click to reveal. Click that, and you will be given the auth token for your bot account, and paste it into the config file.

### LINK REDDIT ACCOUNT TO BOT 

Go to https://www.reddit.com/prefs/apps/ scroll down and click on create application. Copy the clientID and secret ID to the config file under RedditLogin and also type your credentials that is your userID and password.

### RUNNING THE BOT 

Type in the following command: 
```bash 
sudo ./run.sh
```

This is will do it. Now you can have fun with the bot.


## THANK YOU 
