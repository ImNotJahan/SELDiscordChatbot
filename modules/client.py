from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance

import discord
from discord.ext import tasks

import modules.handleapi as handleapi
import modules.handlewebhook as handlewebhook

import queue

import asyncio

import re # for input sanitization

noPrefixChannels = []

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
                prefix, prefixLength, dblToken, discordsToken, threadQueue,
                postStatsToBotsGG, botsggToken, postStatsToTopGG, topggToken,
                *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.postStatsToDBL = postStatsToDBL
        self.postStatsToDiscords = postStatsToDiscords
        self.bot = bot
        self.prefix = prefix
        self.prefixLength = prefixLength
        self.discordsToken = discordsToken
        self.dblToken = dblToken
        self.botsggToken = botsggToken
        self.postStatsToBotsGG = postStatsToBotsGG
        self.threadQueue = threadQueue
        self.topggToken = topggToken
        self.postStatsToTopGG = postStatsToTopGG
    
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        print("In " + str(len(self.guilds)) + " servers")
        
        await self.update_statistics()

        self.check_queue.start()
        self.update_statistics.start();

    async def on_message(self, message):
        text = message.content
        
        if message.author == self.user: return # No talking to self
        if message.author.bot: return # No talking to bots

        if(message.channel.id in noPrefixChannels): pass
        elif ((text)[:self.prefixLength] != self.prefix): return # Only responding to commands
        else: text = text[self.prefixLength:]
        
        await message.channel.send(self.generate_response(text))

    def generate_response(self, message):
        user_input = remove_emojis(message)
        
        return self.bot.get_response(message).text.lower()

    async def thank_user(self, user):
        user = await self.fetch_user(user)
        await user.send("thank you for voting for me o(\_ \_)o")
    
    @tasks.loop(seconds=5.0)
    async def check_queue(self):
        try:
            queueResult = self.threadQueue.get_nowait()
        except queue.Empty:
            pass
        else:
            if(queueResult == None):
                pass
            
            elif(queueResult[:2] == "ID"):
                await self.thank_user(int(queueResult[2:]))
                self.threadQueue.put(None)
                
            elif(queueResult[:7] == "CHANNEL"):
                channel = int(queueResult[7:])

                if(channel not in noPrefixChannels):
                    noPrefixChannels.append(channel)
                self.threadQueue.put(None)
                
            elif(queueResult[:8] == "RCHANNEL"):
                channel = int(queueResult[8:])
                
                if(channel in noPrefixChannels):
                    noPrefixChannels.remove(channel)
                self.threadQueue.put(None)

    # Bot list server count posting
    @tasks.loop(hours=1)
    async def update_statistics(self):
        if(self.postStatsToDBL):
            await handleapi.discordBotListAPI(self, self.dblToken)
        if(self.postStatsToDiscords):
            await handleapi.discordsAPI(self, self.discordsToken)
        if(self.postStatsToBotsGG):
            await handleapi.botsggAPI(self, self.botsggToken)
        if(self.postStatsToTopGG):
            await handleapi.topggAPI(self, self.topggToken)
