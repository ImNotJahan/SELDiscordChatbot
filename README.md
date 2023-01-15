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
To add custom conversations to it, edit the corpus/main.yml file and append conversations to the end like this:
```YAML
- - First line
  - Second line
  - Etc.
```
Then run train.py

If you don't want to reinforce the other dialogs in the file however, you could create a new [corpus file](https://chatterbot.readthedocs.io/en/stable/corpus.html) and add dialog to that, then change the code in train.py to only target it.
