from flask import Flask, jsonify, render_template

from Repository import Repository

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)