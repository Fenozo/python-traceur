from flask import Flask, jsonify, session, request, redirect, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send

from maga.Repository import Repository
from flask_session import Session
from maga.module_api_blf import api_blf
from maga.module_web_user import module_web_user
from maga.module_web_main import module_web_main
import json
import datetime

def create_app():
    app = Flask(__name__)
    app.config["SESSION_TYPE"] = "filesystem"
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    Session(app)

    # front = Blueprint('front', __name__, static_folder='/static')
    # assets = Blueprint('assets', __name__, static_folder='/assets')
    # css  = Blueprint('css', __name__, url_prefix='/css')
    # front.register_blueprint(assets)
    # assets.register_blueprint(css)
    # app.register_blueprint(front)

    app.register_blueprint(api_blf)
    app.register_blueprint(module_web_user)
    app.register_blueprint(module_web_main)
    app.config['SECRET_KEY'] = 'mysecret'
    socketio = SocketIO(app, cros_allowed_origins='*')
    return {
        'app': app 
        ,'socketio' : socketio
    }

data = create_app()
app = data['app'] # ceci va être exporté
socketio = data['socketio'] # ceci va être exporté


@socketio.on('message')
def handleMessage(msg):
    print ('Message : ' + str(msg))
    item = json.loads(msg)
    print(item['isConntected'])
    send(msg, broadcast=True)

def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")
