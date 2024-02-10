from flask import Flask
from config import Config
from extensions import session
import databse
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from data.user import User 




def create_app():
    load_dotenv()
    app = Flask(__name__,template_folder='templates')
    print(os.getenv('JWT'))
    #app.config['SECRET_KEY'] = os.getenv('JWT', 'fallback_secret_key')
    app.config['SECRET_KEY'] = 'hardcoded_secret_key_for_testing'
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT")
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # Initialize Extensions
    #socketio.init_app(app)
    jwt = JWTManager(app)
    CORS(
         app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5000", "http://localhost:19000"],
                "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
                "supports_credentials": True,
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
                "expose_headers": ["Content-Type"],
            }
        },
    )

    session.init_app(app)

    print(app.config)
    return app

