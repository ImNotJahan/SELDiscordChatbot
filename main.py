from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import discord
import configparser

# Bot token stored in seperate file for .gitignore
config = configparser.ConfigParser()
config.read('config.ini')
token = config['Settings']['token']

intents = discord.Intents.default()
intents.messages = True

bot = ChatBot('Lain')

bot.set_trainer(ChatterBotCorpusTrainer)
'''    
bot.train(
    "corpus.main",
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english.psychology",
    "chatterbot.corpus.japanese.computers"
)'''

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        # Stops it from talking to itself
        if message.author == client.user:
            return

        if ((message.content)[:1] != ']'):
            return
        
        user_input = message.content[1:]
        bot_response = bot.get_response(user_input)
        print(user_input)
        print(bot_response)
        await message.channel.send(bot_response.text.lower())


client = Client(intents = intents)
client.run(token)
