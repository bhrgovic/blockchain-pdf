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
from datetime import datetime
import time
from data.user import User 

# Create and configure logger for resource monitoring
logger = logging.getLogger('resource_monitoring')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('system_metrics.csv', mode='w')  # Open in write mode to overwrite old data on each run
formatter = logging.Formatter('%(message)s')  # Use custom formatter suitable for CSV
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Write headers to the CSV file
with open('system_metrics.csv', 'w') as f:
    f.write('Timestamp,CPU Frequency (MHz),CPU Usage (%),Memory Usage (%)\n')

def resource_monitoring():
    while True:
        cpu_frequency = psutil.cpu_freq().current if psutil.cpu_freq() else 'Unavailable'
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp},{cpu_frequency},{cpu_usage},{memory.percent}"
        logger.info(log_message)
        time.sleep(5)  # Adjust as needed

app = Flask(__name__)

def start_monitoring():
    thread = threading.Thread(target=resource_monitoring)
    thread.daemon = True
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

