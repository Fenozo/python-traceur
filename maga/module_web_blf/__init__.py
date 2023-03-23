
from maga import  session, request

from flask import Blueprint, render_template
from maga.config import Configuration, SessionService


web_blf = Blueprint('web_blf', __name__)
objectSession = SessionService(session=session)


@web_blf.route('/web/blf/list')
def blf_list():

    config = Configuration()
    ip_address = f"http://{config.getIpServerSocket()}:{config.getPort()}"
    return render_template('blf_list.html', ip_address=ip_address)