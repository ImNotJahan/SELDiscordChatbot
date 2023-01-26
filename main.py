from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord
from discord.ext import tasks

import configparser
import re # for input sanitization

import modules.handleapi as handleapi
import modules.handlewebhook as handlewebhook

import threading

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

webhooksEnabled = parseBool(config["Settings"]["voteWebhooks"])

postStatsToDBL = parseBool(config["Settings"]["postStatsToDBL"])
postStatsToDiscords = parseBool(config["Settings"]["postStatsToDiscords"])

prefix = config["Settings"]["prefix"]
prefixLength = len(prefix)

# Allows bot to read messages
intents = discord.Intents.default()
intents.messages = True

# Emojis crash ChatBot.get_response function
def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def hadBannedWord(text):
    if(text == "I don't want to talk about this..." or
       text == "Lalalalalalala" or
       text == "Be quiet" or
       text[:4] == "IP: "):
        return True;
    return False;

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

# Discord stuff

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        print("In " + str(len(self.guilds)) + " servers")

        if(postStatsToDBL):
            await handleapi.discordBotListAPI(self, dblToken)
        if(postStatsToDiscords):
            await handleapi.discordsAPI(self, discordsToken)

    async def on_message(self, message):
        if message.author == client.user: return # No talking to self
        if message.author.bot: return # No talking to bots
        if ((message.content)[:prefixLength] != prefix): return # Only responding to commands

        user_input = remove_emojis(message.content[prefixLength:])
        
        # This way sentences with banned words aren't learned
        bot.read_only = hadBannedWord(user_input)
        
        bot_response = bot.get_response(user_input).text
        
        bot.read_only = False # i don't think changing read_only works
        
        print(user_input + " : " + bot_response)
        
        await message.channel.send(bot_response.lower())

    async def thank_user(self, user):
        await self.fetch_user(user).send("thank you for supporting me")
        

# Bot list server count posting
@tasks.loop(hours=1)
async def updateDiscordBotListStatistics():
    if(postStatsToDBL):
        await handleapi.discordBotListAPI(client, dblToken)
    if(postStatsToDiscords):
        await handleapi.discordsAPI(client, discordsToken)


client = Client(intents = intents)
webhook = handlewebhook.Webhook(client.thank_user)

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
