from flask import Flask
from config import Config
from extensions import session
import databse
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import psutil
import threading
import logging
import time
from data.user import User 

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='system_monitoring.log', level=logging.INFO, format=LOG_FORMAT, filemode='w')
logger = logging.getLogger('resource_monitoring')

app = Flask(__name__)

def resource_monitoring():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        logger.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory.percent}%")
        time.sleep(10)  # Log every 60 seconds


def start_monitoring():
    thread = threading.Thread(target=resource_monitoring)
    thread.daemon = True  # Daemon thread will shut down when the main thread exits
    thread.start()


def create_app():
    load_dotenv()
    app = Flask(__name__,template_folder='templates')
    #print(os.getenv('JWT'))
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
    start_monitoring()
    #print(app.config)
    return app

