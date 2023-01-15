from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
import discord
import configparser
import random

# Bot token stored in seperate file for .gitignore
config = configparser.ConfigParser()
config.read("config.ini")
token = config["Settings"]["token"]

intents = discord.Intents.default()
intents.messages = True

def select_response(statement, statement_list, storage=None):
    return random.choice(statement_list)

bot = ChatBot("Lain", logic_adapters=
    [{
        "import_path": "chatterbot.logic.BestMatch",
        "default_response": "?",
        "maximum_similarity_threshold": 0.50,
        "response_selection_method": select_response
    }],preprocessors=
    [
        "chatterbot.preprocessors.clean_whitespace"
    ])

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        # Stops it from talking to itself
        if message.author == client.user: return
        if message.author.bot: return
        if ((message.content)[:1] != "]"): return
        
        user_input = message.content[1:]
        bot_response = bot.get_response(user_input).text
        print(user_input + " : " + bot_response)
        await message.channel.send(bot_response.lower())

client = Client(intents = intents)
client.run(token)
