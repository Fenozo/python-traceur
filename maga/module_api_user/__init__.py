import sys
from flask import Blueprint, jsonify, render_template
from maga import  session, request
from maga.BlfRepository import BlfRepository
from maga.config import  SessionService
from maga.Repository import Repository


module_api_user = Blueprint('module_api_user', __name__)
objectSession = SessionService(session=session)
