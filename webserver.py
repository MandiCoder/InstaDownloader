from threading import Thread
from flask import Flask

flask = Flask('')


@flask.route('/')
def index():
    return "Hola pringao :)"


def run():
    flask.run(
        host='0.0.0.0',
        port=8000
    )
    
def keep_alive():
    server = Thread(target=run)
    server.start()