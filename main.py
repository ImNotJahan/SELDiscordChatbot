from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

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
topggToken = config["Tokens"]["topggToken"] # top.gg

webhooksEnabled = parseBool(config["Settings"]["voteWebhooks"])

postStatsToDBL = parseBool(config["Settings"]["postStatsToDBL"])
postStatsToDiscords = parseBool(config["Settings"]["postStatsToDiscords"])
postStatsToBotsGG = parseBool(config["Settings"]["postStatsToBotsGG"])
postStatsToTopGG = parseBool(config["Settings"]["postStatsToTopGG"])

databaseURI = config["Settings"]["databaseURI"]
prefix = config["Settings"]["prefix"]
prefixLength = len(prefix)

# Allows bot to read messages
intents = discord.Intents.default()
intents.messages = True

from chatterbot import comparisons, response_selection, logic

bot = ChatBot("Lain",
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri=databaseURI,
    logic_adapters=
    [{
        "import_path": "chatterbot.logic.BestMatch",
        "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance"
    }, "modules.adapters.HandleBannedWords",
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
                postStatsToBotsGG=postStatsToBotsGG, botsggToken=botsggToken,
                postStatsToTopGG=postStatsToTopGG, topggToken=topggToken)
webhook = handlewebhook.Webhook(threadQueue)

slash = SlashCommand(client,sync_commands=True)
@slash.slash(name="help")
async def test(ctx):
    await ctx.reply("All you need to do is start each of your messages with ] to talk to me")

@slash.slash(name="lain", description="talk to me", options=[
    create_option(name="text", description="what do you want to say?",
    option_type=SlashCommandOptionType.STRING, required=True)])
async def lain(ctx, text):
    message = await ctx.reply("...")
    await message.edit(content=client.generate_response(text))

@slash.slash(name="activatechannel",
    description="let me talk in this channel without a prefix", options=[
    create_option(name="text", description="which channel?",
    option_type=SlashCommandOptionType.CHANNEL, required=True)])
async def lain(ctx, text):
    threadQueue.put("CHANNEL" + str(text.id))
    await ctx.reply("working on it, might take a few seconds")

@slash.slash(name="deactivatechannel",
    description="stop me from talking in a channel without a prefix", options=[
    create_option(name="text", description="which channel?",
    option_type=SlashCommandOptionType.CHANNEL, required=True)])
async def lain(ctx, text):
    threadQueue.put("RCHANNEL" + str(text.id))
    await ctx.reply("working on it, might take a few seconds")

def start_client():
    client.run(token)

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(client.generate_response(message.content))

def start_webhooks():
    webhook.run()

if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=start_client)
    t1.run()

    if(webhooksEnabled):
        t2 = threading.Thread(target=start_webhooks)
        t2.run()
