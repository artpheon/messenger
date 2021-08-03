from flask import Flask, request, abort
import time
from datetime import datetime


def start_app():
    app = Flask(__name__)

    @app.route("/")
    def index_paige():
        return "HELLO"

    @app.route("/sendMessage", methods=['POST'])
    def chat():
        name = request.args["name"]
        text = request.args["text"]

        name_len = len(name)
        text_len = len(text)
        if name_len > 100 or name_len == 0:
            return abort(400)
        if text_len > 1000 or text_len == 0:
            return abort(400)
        message = {
            "name": name,
            "text": text,
            "time": time.time()
        }
        return message

    test_message1 = {
        "text": "Hello, world!",
        "name": "Max",
        "time": time.time()
    }

    test_message2 = {
        "text": "Hello there",
        "name": "John",
        "time": time.time()
    }

    db = [
        test_message1,
        test_message2
    ]

    @app.route("/messages")
    def get_messages():
        after = float(request.args["after"])
        result = []
        for message in db:
            if message["time"] > after:
                result.append(message)
        return {"messages": result}

    app.run()
