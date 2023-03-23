from flask import Blueprint, render_template, request
import socket

from maga.config import Configuration
module_web_main = Blueprint('module_web_main', __name__)


@module_web_main.route("/")
def home():
    liste = []
    hostname = socket.gethostname()
    host_ip_address = socket.gethostbyname(hostname)

    # #dictionnaire de data
    data = {'user': 'Elyon', 'machine': 'windows 11'}

    # for parent, dnames, fnames in os.walk("files/"):
    #     for fname in fnames:
    #         filename = os.path.join(parent, fname)
    #         liste.append(filename)

    # ip_address = '192.168.123.254'
    
    config = Configuration()

    ip_address = f"http://{config.getIpServer()}:{config.getPort()}"
    
    #affichage
    return render_template('home.html'
        , request=request
        , title='Home'
        , data=data
        , ip_address=ip_address
        , liste=liste
        , host_ip_address=host_ip_address)