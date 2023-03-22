import sys
from flask import Blueprint, jsonify, render_template
from maga import  session, request
from maga.BlfRepository import BlfRepository
from maga.config import  SessionService
from maga.Repository import Repository

from maga.UserRepository import UserRepository
from maga.BlfRepository import BlfRepository


api_blf = Blueprint('api_blf', __name__)
objectSession = SessionService(session=session)


apisList = {
    'debut_ramassage' : '192.168.123.1'
    ,'fin_ramassage' : '192.168.123.2'
    ,'debut_emballage' : '192.168.123.3'
    ,'fin_emballage' : '192.168.123.4'
    ,'prepa_expedition' : '192.168.123.5'
    ,'expedition' : '192.168.123.6'
}

class TracerActionManager:
    def __init__(self) -> None:
        self.apisList = {
            'debut_ramassage' : '192.168.123.1'
            ,'fin_ramassage' : '192.168.123.2'
            ,'debu_emballage' : '192.168.123.3'
            ,'fin_emballage' : '192.168.123.4'
            ,'prepa_expedition' : '192.168.123.5'
            ,'expedition' : '192.168.123.6'
        }

    def debut_ramassage(self, blf):
        numblf = str(blf).replace('-', '/')

        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False
        
        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()

        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.debut_ramassage(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'])
        
        return self.dataParser( numblf, user, datas, yesOrNo)
    
    def dataParser(self, numblf, user, datas, yesOrNo):
        return jsonify({
            'connexion': True if objectSession.checked() else False
            ,'blf' : numblf
            , 'user': user
            , 'blfList' : datas
            , 'yesOrNo' : yesOrNo
        })
    
    def fin_ramassage(self, blf, ):
        numblf = str(blf).replace('-', '/')
    
        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False

        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()

        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.fin_ramassage(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'])


        return self.dataParser( numblf, user, datas, yesOrNo)
    
    def debut_emballage(self, blf, ):
        numblf = str(blf).replace('-', '/')
        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False
        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()
        
        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.debut_emballage(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'], status = blfRepository.DEm)

        return self.dataParser( numblf, user, datas, yesOrNo)
    def fin_emballage(self, blf, ):
        numblf = str(blf).replace('-', '/')
        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False
        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()

        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.fin_emballage(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'])

        return self.dataParser( numblf, user, datas, yesOrNo)
    
    def prepa_expedition(self, blf, ):
        numblf = str(blf).replace('-', '/')
        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False
        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()

        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.prepa_expedition(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'])


        return self.dataParser( numblf, user, datas, yesOrNo)
    def expedition(self, blf):
        numblf = str(blf).replace('-', '/')
        blfRepository = BlfRepository()
        user = None
        datas = []
        yesOrNo = False
        objectSession.setIp(request.environ['REMOTE_ADDR'])
        objectSession.updateKeys()

        if objectSession.checked():
            user = objectSession.get()
            if blfRepository.expedition(numblf=numblf, userId=user['ID']):
                yesOrNo = True
            datas = blfRepository.getListByUser(ID=user['ID'])


        return self.dataParser( numblf, user, datas, yesOrNo)

traceurManager = TracerActionManager()

@api_blf.route("/api/traitementblf/<blf>")
def route_traite_blf(blf):
    numblf = str(blf).replace('-', '/')

    return jsonify({
        'ip' : request.environ['REMOTE_ADDR']
    })


@api_blf.route("/api/traitement/<blf>/<ip>")
def traitement(blf, ip =''):
    
    if str(ip) =='192.168.123.1':
        return traceurManager.debut_ramassage(blf=blf)
    
    if str(ip) =='192.168.123.2':
        return traceurManager.fin_ramassage(blf=blf)
    
    if str(ip) =='192.168.123.3':
        return traceurManager.debut_emballage(blf=blf)
    
    if str(ip) =='192.168.123.4':
        return traceurManager.fin_emballage(blf=blf)
    
    if str(ip) =='192.168.123.5':
        return traceurManager.prepa_expedition(blf=blf)
    
    if str(ip) =='192.168.123.6':
        return traceurManager.expedition(blf=blf)


@api_blf.route("/api/debutramassage/<blf>")
def route_debut_ramassage(blf, userId=''):
    return traceurManager.debut_ramassage(blf=blf)



@api_blf.route("/api/finramassage/<blf>")
def route_fin_ramassage(blf, ):
    return traceurManager.fin_ramassage(blf=blf)


@api_blf.route("/api/debutemballage/<blf>")
def route_debut_emballage(blf, ):
    return traceurManager.debut_emballage(blf=blf)


    
@api_blf.route("/api/finemballage/<blf>")
def route_fin_emballage(blf, ):
    return traceurManager.fin_emballage(blf=blf)



@api_blf.route("/api/prepaexpedition/<blf>")
def route_prepa_expedition(blf, ):
    return traceurManager.prepa_expedition(blf=blf)



@api_blf.route("/api/expedition/<blf>")
def route_expedition(blf, ):
    return traceurManager.expedition(blf=blf)

# def dataParser( numblf, user, datas, yesOrNo):
#     return jsonify({
#         'connexion': True if objectSession.checked() else False
#         ,'blf' : numblf
#         , 'user': user
#         , 'blfList' : datas
#         , 'yesOrNo' : yesOrNo
#     })



@api_blf.route("/api/blflist")
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