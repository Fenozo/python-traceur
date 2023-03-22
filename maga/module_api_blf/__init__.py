import sys
from flask import Blueprint, jsonify, render_template
from maga import session, request
from maga.config import  SessionService


api_blf = Blueprint('api_blf', __name__)
objectSession = SessionService(session=session)