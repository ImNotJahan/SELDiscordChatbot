# SELDiscordChatbot
Discord chatbot written in python intended to immitate Lain from SEL.

## Features
* The more people talk to it, the better its conversing gets
* Easy to add specific dialog to it, look [here](#adding-conversations)
* Let's all love Lain

## Setting up
The chatterbot and discord.py libraries are required

You need to create a config.ini file too include your discord bot token in, with the following format:
```INI
[Settings]
token = <token>
```

If you want a cleaned up dataset for its dialog, you can delete the db.sqlite3 file and run the train.py file.

Then you just run main.py and it will start

## Adding conversations
To add custom conversations to it, edit the corpus/custom.yml file and append conversations to the end like this:
```YAML
- - First line
  - Second line
  - Etc.
```
You need to edit train.py so that the only option in bot.train is "corpus.custom" and then run train.py

You could just run train.py without editing it, but it'll reinforce the other dialogs making the custom dialog rarer
