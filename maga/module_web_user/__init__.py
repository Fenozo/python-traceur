from flask import Blueprint, jsonify, redirect, render_template, url_for
import socket
from maga import  session, request
from maga.config import Configuration, SessionService

from maga.UserRepository import UserRepository
from maga.BlfRepository import BlfRepository
import bcrypt



web_user = Blueprint('web_user', __name__)
objectSession = SessionService(session=session)


@web_user.route('/web/user/list')
def user_list():
    return render_template('user_list.html')


@web_user.route("/web/user/inscription")
def user_register():
    if 'name' in request.args and 'password' in request.args:
        login = request.args['login']
        password = request.args['password']
        password_confim = request.args['password_confim']
        
        if password == password_confim:
            # converting password to array of bytes
            bytes = password.encode('utf-8')

            # generating the salt
            salt = bcrypt.gensalt()

            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)

            user = UserRepository()
            user.register(_name=login,  _password=hash)

        else:
            return redirect(url_for('error le mot de pass n\'est pas confirmé ',name = user_register))

        
    return render_template('users/user_register.html')