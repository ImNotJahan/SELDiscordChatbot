from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord
from discord.ext import tasks

import configparser
import re # for input sanitization

import modules.handleapi as handleapi
#import modules.handlewebhook as handlewebhook

# Bot token stored in seperate file for .gitignore
config = configparser.ConfigParser()
config.read("config.ini")
token = config["Settings"]["token"]
dblToken = config["Settings"]["dblToken"] # dbl : Discord bot list

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
        await handleapi.discordBotListAPI(self, dblToken);

    async def on_message(self, message):
        if message.author == client.user: return # No talking to self
        if message.author.bot: return # No talking to bots
        if ((message.content)[:1] != "]"): return # Only responding to commands

        user_input = remove_emojis(message.content[1:])
        
        # This way sentences with banned words aren't learned
        bot.read_only = hadBannedWord(user_input)
        
        bot_response = bot.get_response(user_input).text

        bot.read_only = False
        
        print(user_input + " : " + bot_response)
        
        await message.channel.send(bot_response.lower())

@tasks.loop(hours=24)
async def updateDiscordBotListStatistics():
    await handleapi.discordBotListAPI(client, dblToken);

client = Client(intents = intents)
#client.run(token)
