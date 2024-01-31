from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_session import Session
from flask_cors import CORS
from logic.networking import PeerNetwork
from utils.blockchain_utils import load_blockchain_from_file
from logic.pbft import PBFT
from logic.transaction_pool import TransactionPool

socketio = SocketIO()
login_manager = LoginManager()
jwt = JWTManager()
session = Session()
cors = CORS()
network = PeerNetwork()
pbft_instance = PBFT()
file_blockchain = load_blockchain_from_file('blockchain.json')
pool = TransactionPool(file_blockchain)