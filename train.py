from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot('Lain')

trainer = ChatterBotCorpusTrainer(bot)
    
'''bot.train(
    "corpus.conversations",
    "corpus.personal",
    "corpus.greetings",
    "corpus.psyche",
    "corpus.tech",
    "corpus.politics",
    "corpus.people",
    "corpus.religion",
    "corpus.custom"
)
'''
trainer.train("./export.json")
