import sys
from flask import Blueprint, jsonify, render_template
from maga import  session, request
from maga.BlfRepository import BlfRepository
from maga.config import  DbManager, SessionService
from maga.Repository import Repository

from maga.UserRepository import UserRepository
from maga.BlfRepository import BlfRepository

db = DbManager()

api_user = Blueprint('api_user', __name__)
objectSession = SessionService(session=session)

class User:
    def __init__(self, ID='', name='', prenom='', profil='', user=''):
        self.ID     = ID
        self.name   = name
        self.prenom = prenom
        self.profil = profil
        self.user   = user

    def exist(self):
        return True if self.ID else False

    def getObject(self):
        return {
            'ID'        : self.ID.strip()
            , 'user'    : self.user
            ,'nom'      : self.name
            ,'prenom'   : self.prenom
            ,'profil'   : self.profil.strip()
        }

    def parserId(self, userId):
        userId = str(userId)
        userId = userId.split('pers-')
        return userId[1]

@api_user.route("/api/login/<userId>", methods=["GET", "POST"])
def login(userId):
    objectUser =  User() # Instanciation de l'objet

    userId = objectUser.parserId(userId)
    fromWhere = None

    objectSession.setIp(request.environ['REMOTE_ADDR'])
    objectSession.updateKeys()
    
    sessionUserId = None
    if objectSession.checked(): # si il y a déjà quelqu'un qui est connecté
        ses = objectSession.get()
        # print('User id ', objectSession.getId(), 'id ', ses['ID'], 'from http ' , userId)
        if ses['ID'] == userId:
            objectUser =  User(ID=ses['ID'], name=ses['name'], prenom=ses["prenom"], profil=ses['profil'] ) # affection de l'objet objectUser
        else:
            objectSession.delete() # déconnecter l'utilisateur de son session

    # l'utilisateur n'est pas encore connété avant alors == False ? print('=> => ', objectSession.checked())
    if objectSession.checked() == False: # si False on le cherche dans la base de données
        userRepository = UserRepository()
        userChecked = userRepository.loginFromQrcode(userId=userId)
        if userChecked is not None: # si l'utilisateur existe par son ID alors on affecte l'utilisateur par un nouveau objet
            objectUser = User(ID=userChecked.ID, user=userChecked.User, name=userChecked.Nom, prenom=userChecked.Prenom, profil=userChecked.Profil)
            objectSession.set(userChecked)
            fromWhere = 'DB'

    else :
        fromWhere = 'SESSION'
    # userChecked = objectUser.getObject() if objectUser.exist()  else False
    blfRepository = BlfRepository()
    blfList = []
    if objectSession.checked():
        user = objectSession.get()
        blfList = blfRepository.getListByUser(ID=user['ID'])

    return jsonify({
        'connexion' : True if objectUser.exist()  else False
        ,'fromWhere' : fromWhere
        , 'user' : objectSession.get()
        ,'blfList' : blfList
        ,'ip' : request.remote_addr
        , 'realIp' : request.environ['REMOTE_ADDR']
    })


@api_user.route('/api/user/list')
def listUser():
    conn = db.get_instance()
    cursor = conn.cursor()
    sql = f"""--begin-sql 
        SELECT * FROM  Aya_Users
        --end-sql
    """
    cursor.execute(sql)

    users = cursor.fetchall()

    my_datas = []

    for u in users:
        d = User(ID=u.ID, user=u.User, name=u.Nom, prenom=u.Prenom, profil=u.Profil)
        my_datas.append(d.getObject())

    
    return jsonify({
        'connexion' : True
        , 'data' : my_datas
    })

@api_user.route("/api/logout")
def logout ():
    # objectUser =  User() # Instanciation de l'objet
    # userId = objectUser.parserId(userId)
    objectSession.setIp(request.environ['REMOTE_ADDR'])
    objectSession.updateKeys()
    objectSession.delete()

    try:
        return jsonify({
            'connexion' : False
            ,'status' : 'deconnected'
            ,'user' : None
        })
    except:
        return jsonify({
            'connexion' : True
            ,'status' : 'connected'
            ,'user' : None
        })
