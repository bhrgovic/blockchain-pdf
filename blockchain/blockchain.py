import json
import base64
import PyPDF2
import socket
import threading
from .pbft import PBFT
from .networking import PeerNetwork


class FileBlockchain:
    def __init__(self, is_primary=False):
        self.chain = []
        self.is_primary = is_primary
        self.transaction_pool = []
        self.pbft = PBFT()
        self.network = PeerNetwork()

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)
        if len(self.transaction_pool) >= 3:  # Assume 3 transactions per block
            new_block = self.create_new_block()
            self.network.broadcast_pre_prepare(new_block, self.pbft, self)

    def create_new_block(self):
        new_block = {"index": len(self.chain), "transactions": self.transaction_pool}
        self.transaction_pool = []
        return new_block

    def set_primary(self, is_primary):
        self.is_primary = is_primary

    def pre_prepare(self, new_block):
        if self.is_primary:
            # Validate the new block (assuming validate_block is a method you've implemented)
            if self.validate_block(new_block):
                self.current_phase = "pre-prepare"
                # Broadcast pre-prepare message to all peers
                # For the example, we'll print it
                print(f"Broadcasting pre-prepare message for block {new_block}")
                return True
        return False

    def prepare(self, pre_prepare_msg):
        # Validate pre-prepare message and check if it matches the block
        if self.validate_pre_prepare(pre_prepare_msg):
            self.current_phase = "prepare"
            self.prepare_count += 1
            # Broadcast prepare message to all peers
            # For the example, we'll print it
            print(f"Broadcasting prepare message for block {pre_prepare_msg}")
            return True
        return False

    def commit(self):
        # Check if we have received 2f + 1 prepare messages (simplified)
        # In a real-world scenario, these messages would be validated
        if self.prepare_count >= 2:
            self.current_phase = "commit"
            self.commit_count += 1
            # Broadcast commit message to all peers
            # For the example, we'll print it
            print("Broadcasting commit message")
            return True
        return False

    def reply(self):
        # Check if we have received 2f + 1 commit messages (simplified)
        # In a real-world scenario, these messages would be validated
        if self.commit_count >= 2:
            self.current_phase = "reply"
            # Add the block to the blockchain
            # For the example, we'll add a dummy block
            self.chain.append({"index": len(self.chain), "data": "dummy"})
            print("Added block to the blockchain")
            return True
        return False

    def validate_block(self, block):
        # Implement your own validation logic
        return True

    def validate_pre_prepare(self, pre_prepare_msg):
        # Implement your own validation logic
        return True
    
    def add_pdf_to_blockchain(self, pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            if pdf_reader.getNumPages() > 2:
                print("PDF is too long. Only 1-2 pages are allowed.")
                return

            f.seek(0)  # Seek to the start of the file
            pdf_data = f.read()

        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")

        new_block = {
            'index': len(self.chain) + 1,
            'pdf_base64': pdf_base64
            # Add other block data like timestamp, previous hash, etc.
        }

        self.chain.append(new_block)

    def read_pdf_from_blockchain(self, index):
        block = self.chain[index]
        pdf_base64 = block.get("pdf_base64")
        if not pdf_base64:
            print("No PDF found in this block.")
            return

        pdf_data = base64.b64decode(pdf_base64)
        pdf_path = f"block_{index}_pdf.pdf"

        with open(pdf_path, "wb") as f:
            f.write(pdf_data)

        print(f"PDF extracted to {pdf_path}")


    def run_server(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        
        self.peers.add((host, port))  # Add self to peer list
        
        print(f"Server running on {host}:{port}")

        while True:
            client_socket, address = server.accept()
            print(f"Accepted connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            
    def handle_client(self, client_socket):
        # Your existing code to handle incoming data, sync blockchain etc.
        
        # Send the list of known peers to the client
        client_socket.send(json.dumps(list(self.peers)).encode())

        # Your existing code to handle incoming data, sync blockchain etc.

    def connect_to_peer(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        # Receive data from server, which includes its peer list
        data = client.recv(1024).decode()
        new_peers = json.loads(data)
        
        # Add the new peers to the known peer list
        self.peers.update(new_peers)
        
        # Continue with your existing code to handle blockchain synchronization etc.
        
    def discover_peers(self):
        # Connect to all known peers to update the peer list
        for peer in list(self.peers):
            host, port = peer
            self.connect_to_peer(host, port)


    # Add your PBFT or consensus logic here...
