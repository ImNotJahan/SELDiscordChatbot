import discord
import requests

async def discordBotListAPI(client, dblToken):
    clientID = client.user.id
    authToken = dblToken
    guilds = f"{len(client.guilds)}"
    
    r = requests.post(
        f"https://discordbotlist.com/api/v1/bots/{clientID}/stats",
        headers={"Authorization":f"{authToken}"}, 
        data={"guilds":f"{guilds}"}
    )
