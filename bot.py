import discord
import sys
from discord import channel
from discord.ext import commands
from praw.models.listing.mixins import subreddit
from praw.reddit import Reddit, Subreddit
import logger
import logging
import configparser
import os.path
from shutil import copyfile
import time
import praw


logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")



if not os.path.isfile("config.ini"):
    try:
        copyfile("default_config.ini", "config.ini")
        logger.log("Config file config.ini not found, generating a new one from default_config.ini", "warning")
    except:
        logger.log("Neither config.ini , nor default_config.ini do not exist, cannot create bot." , "CRITICAL")
        sys.exit(1)


config = configparser.ConfigParser()
config.read("config.ini")
logger.log("Config file loaded" , "info")


#load all the values from config file 
try:
    token = config["Login"]["token"]
    redditUser = config["RedditLogin"]["username"]
    redditPassword = config["RedditLogin"]["password"]
    redditID = config["RedditLogin"]["client_id"]
    redditSecret = config["RedditLogin"]["client_secret"]
    botCommandPrefix = config["Options"]["command_prefix"]
except:
    logger.log("Wrong config format. Please make it same as default_config.ini ", "error")
    sys.exit(1)



#Log in to reddit to reddit and authenticate the account
try:
    reddit = praw.Reddit(client_id=redditID, client_secret=redditSecret, password=redditPassword, username=redditUser, user_agent='hel' , check_for_async = False)
    reddit.user.me()
    logger.log("Logged in to reddit with username u/"+redditUser )
except:
    logger.log("Wrong reddit credentials." "error")
    sys.exit(1)


bot = commands.Bot(command_prefix=botCommandPrefix)
categories = ["top" , "new"  , "best" , "rising" , "controversial"]



#fetches 5 posts from the subreddit
def fetchPosts(subredditName: str, limit: int, categ: str):
    if categ == "top":
        return reddit.subreddit(subredditName).top(limit=limit)
    elif categ == "new":
        return reddit.subreddit(subredditName).new(limit=limit)
    elif categ == "controversial":
        return reddit.subreddit(subredditName).controversial(limit=limit)
    elif categ == "rising":
        return reddit.subreddit(subredditName).rising(limit=limit)
    elif categ == "best":
        return reddit.subreddit(subredditName).best(limit = limit)



#makes embed for discord 
def getEmbed(post):
    try:
        embed = discord.Embed()
        embed.title = post.title
        # embed.url = "https://www.reddit.com" + post.permalink
        embed.description = post.selftext[:2040]
        if not post.is_self:
            if post.url.lower().endswith((".jpeg", ".jpg", ".png", ".gif")):
                embed.set_thumbnail(url=post.url)
                postTypeStr = "link (image)"
            else:
                embed.add_field(name="Link from post:", value=post.url, inline=True)
                postTypeStr = "link"
        else:
            postTypeStr = "self-post (text)"
        embed.colour = discord.Colour(0).from_rgb(255, 86, 0)
        embed.set_footer(text="/u/" + post.author.name + ", " + postTypeStr,  icon_url=post.author.icon_img)
        return embed
    except Exception as e:
        logger.exception(e)
        return 




@bot.event
async def on_ready():
    logger.log("Bot initialized. Logging in...")
    logger.log('Logged in as ' + bot.user.name + ' with ID [' + str(bot.user.id) + '] on:')
    

@bot.command()
async def hello(message : discord.Message):
    await message.channel.send("hello")
    logger.log("Said hello to "+str(message.author))


@bot.command(help ="!send [category] [subreddit]\n category = best/top/new/rising/hot/controversial\n subreddit = subreddit's name ")
async def send(message : discord.Message , *args):
    if(len(args) != 2 or args[0] not in categories):
        logger.log("invalid Syntax")
        help(message)
        return

    
    try: 
        for post in fetchPosts(args[1] , 5 , args[0]):
            await message.channel.send(embed = getEmbed(post))

        logger.log("Posted "+ args[0] +" from r/" + args[1] + " for "+ str(message.author))
    except Exception as e:
        logger.exception(e)
        await message.channel.send("Error occured! Check the log file.")

    


    



try:
    bot.run(token)
except Exception as e:
    logger.log("There was an error while connecting the bot to Discord. Your token might be invalid or you can't connect to Discord's servers." ,"critical")
    logger.exception(e)
    time.sleep(5)
    sys.exit(1)
