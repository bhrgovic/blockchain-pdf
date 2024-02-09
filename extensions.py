from flask_socketio import SocketIO

from flask_session import Session
from flask_cors import CORS
from logic.networking import PeerNetwork
from logic.blockchain import FileBlockchain
from logic.pbft import PBFT


socketio = SocketIO()


session = Session()
cors = CORS()
network = PeerNetwork()
total_nodes=len(network.peers)
pbft_instance = PBFT(total_nodes=total_nodes)
file_blockchain = FileBlockchain()
blockchain =file_blockchain.load_blockchain_from_mongodb()
