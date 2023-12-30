from api.app import app,socketio,file_blockchain
from logic import blockchain   # Update this import based on your project structure
import threading
import time

# Separate thread for peer discovery and blockchain updating
def manage_peers_and_chain():
    while True:
        print("Discovering peers...")
        file_blockchain.discover_peers()
        
        print("Updating blockchain...")
        file_blockchain.update_chain()
        


if __name__ == '__main__':
    socketio.run(app)

    # Initialize the background thread
    #background_thread = threading.Thread(target=manage_peers_and_chain)
    #background_thread.daemon = True
    #background_thread.start()