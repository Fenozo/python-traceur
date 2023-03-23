from maga import socketio, app
from maga.config import Configuration
config = Configuration()
if __name__ == '__main__':
    socketio.run(app=app,debug=True, allow_unsafe_werkzeug=True, host=f'{config.getIpServer()}', port=f'{config.getPort()}')