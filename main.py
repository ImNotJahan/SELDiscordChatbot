from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord

import configparser

import asyncio

import modules.handlewebhook as handlewebhook
from modules.client import Client

import threading, queue

def parseBool(text):
    if(text == "true"):
        return True
    return False # False is also default

# Bot token stored in seperate file for .gitignore
config = configparser.ConfigParser()
config.read("config.ini")
token = config["Tokens"]["discordToken"]
dblToken = config["Tokens"]["dblToken"] # dbl : Discord bot list
discordsToken = config["Tokens"]["discordsToken"] # discords.com
botsggToken = config["Tokens"]["botsggToken"] # discord.bots.gg

webhooksEnabled = parseBool(config["Settings"]["voteWebhooks"])

postStatsToDBL = parseBool(config["Settings"]["postStatsToDBL"])
postStatsToDiscords = parseBool(config["Settings"]["postStatsToDiscords"])
postStatsToBotsGG = parseBool(config["Settings"]["postStatsToBotsGG"])

prefix = config["Settings"]["prefix"]
prefixLength = len(prefix)

# Allows bot to read messages
intents = discord.Intents.default()
intents.messages = True

bot = ChatBot("Lain", logic_adapters=
    [{
        "import_path": "chatterbot.logic.BestMatch",
        "default_response": "?",
        "maximum_similarity_threshold": 0.95,
        "response_selection_method": "chatterbot.response_selection.get_random_response"
    }, "modules.adapters.HandleBannedWords",
    {
        "import_path": "chatterbot.logic.SpecificResponseAdapter",
        "input_text": "help",
        "output_text": "All you need to do is start each of your messages with ] to talk to me"
    }
    ], preprocessors=
    [
        "chatterbot.preprocessors.clean_whitespace"
    ])

threadQueue = queue.Queue() # I hate multithreading

# I need to fix the amount of parameters
client = Client(intents=intents, bot=bot,
                postStatsToDBL=postStatsToDBL, postStatsToDiscords=postStatsToDiscords,
                prefix=prefix, prefixLength=prefixLength, discordsToken=discordsToken,
                dblToken=dblToken, threadQueue=threadQueue,
                postStatsToBotsGG=postStatsToBotsGG, botsggToken=botsggToken)
webhook = handlewebhook.Webhook(threadQueue)

def start_client():
    client.run(token)

def start_webhooks():
    webhook.run()

if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=start_client)
    t1.start()

    if(webhooksEnabled):
        t2 = threading.Thread(target=start_webhooks)
        t2.start()
