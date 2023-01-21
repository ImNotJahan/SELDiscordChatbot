from flask import Flask, request
import json
import discord

app = Flask(__name__)

def default(a):
    print("default")

func = default

class Webhook:
    def __init__(self, funca):
        global func
        func = funca
    
    @app.route("/dblupvote", methods=['POST'])
    def handleDBLUpvote():
        data = json.loads(request.data)
        print("Upvoted by {}, ID {}".format(data["username"], data["id"]))

        func(int(data["id"]))
        return "OK"

    def run(self):
        app.run(host='0.0.0.0', port=7800, ssl_context="adhoc")
