from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot('Lain')

bot.set_trainer(ChatterBotCorpusTrainer)
    
bot.train(
    "corpus.main"
)
