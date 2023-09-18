import threading
import json
import socket

class Server:

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
        
        