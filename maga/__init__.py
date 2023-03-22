from flask import Flask, jsonify, session, request, redirect, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
from maga.Repository import Repository
from flask_session import Session
from maga.module_api_blf import api_blf

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
    app.config['SECRET_KEY'] = 'mysecret'
    socketio = SocketIO(app, cros_allowed_origins='*')
    return {
        'app': app 
        ,'socketio' : socketio
    }

data = create_app()
app = data['app'] # ceci va être exporté
socketio = data['socketio'] # ceci va être exporté


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/api/blflist")
def route_blf():
    liste = []

    repository = Repository()
    
    # conn = db.get_instance()
    # cursor = conn.cursor()
    sql = f"""--begin-sql 
        /****** Script de la commande SelectTopNRows à partir de SSMS  ******/
        SELECT TOP 5000 [numblf]
            ,[sd_ram]
            ,[st_ram]
            ,[rs_ram] -- responsable start ramassage
            ,[re_ram] -- responsable fin ramassage
            ,[ed_ram] -- date fin ramassage
             ,[se_ram] -- temps fin ramassage
            ,[rs_em]-- responsable start emballage
            ,[re_em] -- responsable fin emballage
            , [sd_em] -- début emballage
            , [st_em] -- début temps emballage
            ,[resp_prepa_exp]
            ,[resp_exp]
            ,[statut]
        FROM [Commerciale].[dbo].[aya_magasin_tache_table]
        --end-sql
    """
    # cursor.execute(sql)

    blf_lists = repository.getList(sql=sql)
    my_datas = []



    # #dictionnaire de data
    for data in blf_lists:
        my_datas.append({
            'NumBlf'            : data.numblf
            , 'debutRam'        : f"{data.sd_ram}"
            ,'FinRam'           : f"{data.ed_ram}"
            , "tempFinRam"      : f"{data.se_ram}"
            ,'respRam'          : f"{data.rs_ram}"
            ,'respFinRam'       : f"{data.re_ram}"
            ,'debutEmballage'   : f"{data.sd_em}"
            ,'debutTempsEm'   : f"{data.st_em}"
            ,'statut' : data.statut
        })

    return jsonify({
        'connexion' : True
        ,'data' : my_datas
        })
