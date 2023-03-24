import sys
from flask import Blueprint, jsonify, render_template
from maga import  session, request
from maga.BlfRepository import BlfRepository
from maga.config import  SessionService
from maga.Repository import Repository
import math
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



@api_blf.route("/api/blflist/<page_0>")
def route_blf(page_0=1):
    PageNo = int(page_0)
    if 'pageNumber' in request.args:
        PageNo = int(request.args['pageNumber'])


    liste = []

    repository = Repository()
    # conn = db.get_instance()
    # cursor = conn.cursor()
    sql = f"""--begin-sql 
        /****** Script de la commande SelectTopNRows à partir de SSMS  ******/
        --DECLARE @PageNo  INT=10
DECLARE @PageSize INT=10

select  T.RowNum, T.nb_blf, id_traceur, numblf , Nom_personnel, MatSaisie, Prefixe, Rs, CP, District, Province
            ,NBLG
            ,DateSaisie
            , [sd_ram]
            , [st_ram]
            , [rs_ram] -- responsable start ramassage
            , [re_ram] -- responsable fin ramassage
            , [ed_ram] -- date fin ramassage
            , [se_ram] -- temps fin ramassage
            , [rs_em]-- responsable start emballage
            , [re_em] -- responsable fin emballage
            , [sd_em] -- début emballage
            , [st_em] -- début temps emballage
            , [et_em] -- fin temps emballage
            , [ed_em] -- fin date emballage
            , [resp_prepa_exp]
            , [date_prepa_exp]
            , [time_prepa_exp]
            , [date_exp]
            , [time_exp]
            , [resp_exp]
            ,[statut]
            ,montant_ca_brut
            ,nblh
            , lieu_stockage 
from(

	select id_traceur, numblf , Nom_personnel, MatSaisie, Prefixe, Rs, CP, District, Province
    ,NBLG
    ,DateSaisie
	,[sd_ram]
            , [st_ram] -- start time ramassage
            , [rs_ram] -- responsable start ramassage
            , [re_ram] -- responsable fin ramassage
            , [ed_ram] -- date fin ramassage
            , [se_ram] -- temps fin ramassage
            , [rs_em]-- responsable start emballage
            , [re_em] -- responsable fin emballage
            , [sd_em] -- début emballage
            , [st_em] -- début temps emballage
            , [et_em] -- fin temps emballage
            , [ed_em] -- fin date emballage
            , [resp_prepa_exp]
            , [date_prepa_exp]
            , [time_prepa_exp]
            , [date_exp]
            , [time_exp]
            , [resp_exp]
            , [statut]
            , montant_ca_brut
            , nblh
            , lieu_stockage
            , (select COUNT(*)  from aya_magasin_tache_table)  as nb_blf
	, ROW_NUMBER() over (order by numblf) as RowNum
	from [aya_magasin_tache_table]

    --end-sql"""

    # search_by_value = None
    if 'search_by_value' in request.args:
        search_by_value = request.args['search_by_value']
        sql = sql + f"""--begin-sql
            where numblf like '%{search_by_value}%'
        --end-sql"""

    sql = sql + f"""
    --begin-sql
    )T 
    WHERE T.RowNum BETWEEN (({PageNo-1}) * @PageSize)+1 AND ({PageNo} * @PageSize) order by T.RowNum ASC
    --WHERE T.RowNum BETWEEN ((@PageNo-1) * @PageSize)+1 AND (@PageNo * @PageSize) order by id_traceur ASC


        --end-sql
    """
    # cursor.execute(sql)

    print(sql)

    blf_lists = repository.getList(sql=sql)
    my_datas = []

    my_pagination = {
        'state' : None
        ,'totalNumber' : 0
        , "pageSize"  : 0
        , "currentPage" : 0
    }

    # #dictionnaire de data
    if blf_lists is not None:
        for data in blf_lists:
            if my_pagination['state'] is None:
                my_pagination = {
                    'state' : True
                    ,'totalNumber'           : f"{data.nb_blf}"
                    , "pageSize"             : math.ceil((data.nb_blf) /10)
                    , "currentPage"          :   PageNo
                } 
            my_datas.append({
                'id'                : f"{data.RowNum}"
                ,'NumBlf'            : data.numblf
                
                , 'mom_personnel'   : f"{data.Nom_personnel}"
                , 'date_saisie'     : f"{data.DateSaisie}"
                , 'saisie'          : f"{data.MatSaisie}"
                , "prefixe"         : f"{data.Prefixe}"
                , 'rs'              : f"{data.Rs}"
                , "client"          : f"{data.Prefixe} {data.Rs}"
                , "district"        : f"{data.District}"
                , "province"        : f"{data.Province}"
                , "nblg"            : f"{data.NBLG}"
                , 'nblh'            : f"{data.nblh}"
                , "lieu_stockage"   : f"{data.lieu_stockage}"
                , "montant_ca_brut" : f"{data.montant_ca_brut}"
                , "ramassage" :  {
                    'start_time'      : f"{data.st_ram}"
                    , 'start_date'    : f"{data.sd_ram}"
                    , 'start_resp'    : f"{data.rs_ram}"
                    , "end_time"      : f"{data.se_ram}"
                    , 'end_date'      : f"{data.ed_ram}"
                    , 'end_resp'      : f"{data.re_ram}"
                }
                , "emballage" : {
                    "start_date"    : f"{data.sd_em}"
                    , "start_time"  : f"{data.st_em}"
                    , "end_time"    : f"{data.et_em}"
                    , "end_date"    : f"{data.ed_em}"
                    , "start_resp"  : f"{data.rs_em}"
                    , "end_resp"    : f"{data.re_em}"
                }
                ,'prepa_expedition'   : {
                    "date"              :  f"{data.date_prepa_exp}"
                    ,"time"              :  f"{data.time_prepa_exp}"
                    ,"responsable"      :  f"{data.sd_em}" 
                }
                , "expedition" : {
                    "date"          : f"{data.date_exp}"
                    , "time"        : f"{data.time_exp}"
                    ,"responsable"  : f"{data.resp_exp}"
                }
                ,'debutTempsEm'     : f"{data.st_em}"
                ,'statut'           : data.statut
                
            })

    return jsonify({
        'connexion' : True
        , 'pagination' : my_pagination
        ,'items' : my_datas
        })