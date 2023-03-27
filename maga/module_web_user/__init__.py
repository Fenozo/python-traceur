from flask import Blueprint, jsonify, render_template
import socket
from maga import  session, request
from maga.config import Configuration, SessionService

from maga.UserRepository import UserRepository
from maga.BlfRepository import BlfRepository


web_user = Blueprint('web_user', __name__)
objectSession = SessionService(session=session)


@web_user.route('/web/user/list')
def user_list():
    return render_template('user_list.html')


@web_user.route("/web/user/inscription")
def user_register():
    if 'name' in request.args and 'password' in request.args:
        name = request.args['name']
        password = request.args['password']
        print({
            'name' : name
            ,'password' : password
        })
    return render_template('users/user_register.html')