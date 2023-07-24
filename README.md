# SELDiscordChatbot
Discord chatbot written in python intended to imitate Lain from SEL.

## Features
* The more people talk to it, the better its conversing gets
* Easy to add specific dialog to it, look [here](#adding-conversations)
* Let's all love Lain

## Setting up
The chatterbot and discord.py libraries are required

You need to create a config.ini file too include your discord bot token in, with the following format:
```INI
[Tokens]
discordToken = <token>
dblToken = [token]
discordsToken = [token]
botsggToken = [token]
topggToken = [token]

[Settings]
prefix = <prefix>
databaseURI = <string>
postStatsToDBL = <bool>
postStatsToDiscords = <bool>
postStatsToBotsGG = <bool>
postStatsToTopGG = <bool>
voteWebhooks = <bool>
```

Run `train.py` and then run `main.py` and it will start
Afterwards all you need to start it is run `main.py`

## Adding conversations
To add custom conversations to it, edit the corpus/custom.yml file and append conversations to the end like this:
```YAML
- - First line
  - Second line
  - Etc.
```
You need to edit train.py so that the only option in bot.train is "corpus.custom" and then run train.py

You could just run train.py without editing it, but it'll reinforce the other dialogs making the custom dialog rarer
