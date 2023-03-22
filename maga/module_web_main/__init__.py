from flask import Blueprint, render_template
import socket

from maga.config import Configuration
module_web_main = Blueprint('module_web_main', __name__)


@module_web_main.route("/")
def home():
    liste = []
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

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
    return render_template('home.html', title='Home', data=data, ip_address=ip_address, liste=liste)