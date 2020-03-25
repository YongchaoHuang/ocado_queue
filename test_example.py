# created by @Heroku & @YongchaoHuang on 24/03/2020

from flask import Flask # pip install flask
from threading import Thread
import logging
import importlib
import web_queue
importlib.reload(web_queue)
from web_queue import web_Queue
logging.basicConfig()
logging.root.setLevel(logging.INFO)

app = Flask(__name__)


queue = web_Queue.GetInstance('https://www.ocado.com/webshop/startWebshop.do')
# queue.run_queue()
init_thread = Thread(target=queue.run_queue)
init_thread.daemon = True
init_thread.start()

@app.route('/heart_beat')
def heart_beat():
    return 'I am online'

@app.route('/')
def show_sessions():
    queue = web_Queue.GetInstance()
    return str(queue.session_bags)

# app.run()
