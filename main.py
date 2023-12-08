from api.app import app
from logic import blockchain   # Update this import based on your project structure
import threading
import time

if __name__ == '__main__':
    app.run(debug=True)

file_blockchain = blockchain.FileBlockchain(is_primary=True)

# Separate thread for peer discovery and blockchain updating
def manage_peers_and_chain():
    while True:
        print("Discovering peers...")
        file_blockchain.discover_peers()
        
        print("Updating blockchain...")
        file_blockchain.update_chain()
        
        time.sleep(60)  # Sleep for 60 seconds

# Initialize the background thread
background_thread = threading.Thread(target=manage_peers_and_chain)
background_thread.daemon = True
background_thread.start()