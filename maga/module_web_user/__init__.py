from flask import Blueprint, jsonify, render_template
import socket
from maga import  session, request
from maga.config import Configuration, SessionService

from maga.UserRepository import UserRepository
from maga.BlfRepository import BlfRepository


module_web_user = Blueprint('module_web_user', __name__)
objectSession = SessionService(session=session)


@module_web_user('/user/list')
def user_list():
    return render_template('user_list.html')