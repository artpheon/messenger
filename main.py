import uuid
import time
import json
from flask import Flask, request, render_template
from datetime import datetime


def start_app():
    app = Flask(__name__)

    db_file = "./data/db.json"
    json_db = open(db_file, "rb")
    data = json.load(json_db)
    db = data["messages"]

    def save_msgs():
        data = {
            "messages": db
        }
        json_db = open(db_file, "w")
        json.dump(data, json_db)

    @app.route("/")
    def index():
        return render_template('./index.html')

    @app.route("/form")
    def form():
        return render_template('./form.html')

    @app.route("/sendMessage")
    def chat():
        name = request.args["name"]
        text = request.args["text"]

        name_len = len(name)
        text_len = len(text)

        if name_len > 100 or name_len == 0:
            return 'ERROR'
        if text_len > 1000 or text_len == 0:
            return 'ERROR'

        message = {
            "id": str(uuid.uuid4()),
            "name": name,
            "text": text,
            "time": time.time()
        }
        db.append(message)
        save_msgs()
        return 'OK'

    def print_msg(messages):
        for message in messages:
            name = message['name']
            txt = message['text']
            msg_time = message['time']
            time_pretty = datetime.fromtimestamp(msg_time)

            print(f'[{name}] / {time_pretty}')
            print(txt)
            print()

    @app.route("/messages")
    def get_messages():
        after = float(request.args["after"])
        result = []
        for message in db:
            if message["time"] > after:
                result.append(message)
        return {"messages": result}

    app.run(host='0.0.0.0', port=8080)


start_app()
