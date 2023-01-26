from flask import Flask, request
import json
import discord
import asyncio

app = Flask(__name__)

def default(a):
    print("default")

func = default

class Webhook:
    def __init__(self, paramThreadQueue):
        global threadQueue
        threadQueue = paramThreadQueue
    
    @app.route("/dblupvote", methods=['POST'])
    def handleDBLUpvote():
        data = json.loads(request.data)
        
        threadQueue.put("ID" + data["id"])
        return "OK"

    def run(self):
        app.run(host='0.0.0.0', port=7800)
