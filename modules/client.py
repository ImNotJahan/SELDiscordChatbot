from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord
from discord.ext import tasks

import modules.handleapi as handleapi
import modules.handlewebhook as handlewebhook

import re # for input sanitization

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

class Client(discord.Client):
    def __init__(self, intents, postStatsToDBL, postStatsToDiscords, bot,
                prefix, prefixLength, dblToken, discordsToken,
                *args, **kwargs):
        self.postStatsToDBL = postStatsToDBL
        self.postStatsToDiscords = postStatsToDiscords
        self.bot = bot
        self.prefix = prefix
        self.prefixLength = prefixLength
        self.discordsToken = discordsToken
        self.dblToken = dblToken

        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        print("In " + str(len(self.guilds)) + " servers")
        
        if(self.postStatsToDBL):
            await handleapi.discordBotListAPI(self, self.dblToken)
        if(self.postStatsToDiscords):
            await handleapi.discordsAPI(self, self.discordsToken)

    async def on_message(self, message):
        if message.author == self.user: return # No talking to self
        if message.author.bot: return # No talking to bots
        if ((message.content)[:self.prefixLength] != self.prefix): return # Only responding to commands

        user_input = remove_emojis(message.content[self.prefixLength:])
        
        # This way sentences with banned words aren't learned
        self.bot.read_only = hadBannedWord(user_input)
        
        bot_response = self.bot.get_response(user_input).text
        
        self.bot.read_only = False # i don't think changing read_only works
        
        print(user_input + " : " + bot_response)
        
        await message.channel.send(bot_response.lower())

    async def thank_user(self, user) -> None:
        await self.fetch_user(user).send("thank you for supporting me")
