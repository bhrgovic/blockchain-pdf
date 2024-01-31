from flask import Flask
from config import Config
from extensions import socketio, jwt, login_manager, session, cors
import databse
from socket_events import register_socketio_events
import os

from data.user import User 

@login_manager.user_loader
def load_user(user_id):
    user = User.load_user(user_id)
    print(user_id)
    return  user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT')

    # Initialize Extensions
    socketio.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    #session.init_app(app)
    cors.init_app(app)
    

    register_socketio_events(socketio)

    # ... additional configurations like error handlers

    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)