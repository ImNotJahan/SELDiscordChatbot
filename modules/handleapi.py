import discord
import requests

async def discordBotListAPI(client, authToken):
    clientID = client.user.id
    guilds = f"{len(client.guilds)}"
    
    r = requests.post(
        f"https://discordbotlist.com/api/v1/bots/{clientID}/stats",
        headers={"Authorization":f"{authToken}"}, 
        data={"guilds":f"{guilds}"}
    )

async def discordsAPI(client, authToken):
    clientID = client.user.id
    guilds = f"{len(client.guilds)}"
    
    r = requests.post(
        f"https://discords.com/bots/api/bot/{clientID}",
        headers={"Authorization":f"{authToken}"}, 
        data={"server_count":f"{guilds}"}
    )

async def botsggAPI(client, authToken):
    clientID = client.user.id
    guilds = f"{len(client.guilds)}"
    
    r = requests.post(
        f"https://discord.bots.gg/api/v1/bots/{clientID}/stats",
        headers={"Authorization":f"{authToken}"}, 
        data={"guildCount":f"{guilds}"}
    )

async def topggAPI(client, authToken):
    clientID = client.user.id
    guilds = f"{len(client.guilds)}"
    
    r = requests.post(
        f"https://top.gg/api/bots/{clientID}/stats",
        headers={"Authorization":f"{authToken}"}, 
        data={"server_count":f"{guilds}"}
    )
