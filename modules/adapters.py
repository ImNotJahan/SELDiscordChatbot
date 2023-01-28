from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import random

bannedWords = open("wordblacklist.txt", "r").read().split(",")

class HandleBannedWords(LogicAdapter):
    def __init__(self, chatbot=None, **kwargs):
        super().__init__(chatbot)

    def can_process(self, statement):
        for word in bannedWords:
            word = word
            if word in statement.text:
                return True
        return False

    def process(self, input_statement):
        rand = random.random()

        if(rand < .4):
            selected_statement = Statement("I don't want to talk about this...")
        elif(rand < .70):
            selected_statement = Statement("Lalalalalalala")
        elif(rand < .9):
            selected_statement = Statement("Be quiet")
        else:
            # Fake doxxing :)
            ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            selected_statement = Statement("IP: " + ip)
            
        selected_statement.confidence = 1 # Adapter should take priority

        return selected_statement
