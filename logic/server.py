import threading
import json
import socket
import blockchain

class Server:

    def __init__(self):
        self.peers = set()  # Initialize an empty set to store peer (host, port) tuples

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
        try:
            # Sending the list of known peers to the client
            client_socket.send(json.dumps({"type": "peer_list", "peers": list(self.peers)}).encode())

            # Continuously listen for data from the client
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    # If data is not received, break
                    print("No data received. Closing connection.")
                    break

                data = json.loads(data)
                if data['type'] == 'transaction':
                    print(f"Received new transaction: {data['transaction']}")
                    # Add the transaction to the transaction pool
                    # Assuming add_transaction_to_pool is a method in your blockchain class
                    blockchain.add_transaction_to_pool(data['transaction'])
                    
                elif data['type'] == 'get_chain_length':
                    print("Received request for blockchain length.")
                    # Return the length of the blockchain
                    # Assuming blockchain is an instance of your FileBlockchain class
                    chain_length = len(blockchain.chain)
                    client_socket.send(json.dumps({"type": "chain_length", "length": chain_length}).encode())

                else:
                    print("Unknown command.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the client socket
            client_socket.close()


    def connect_to_peer(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # Receive data from the server, which includes its peer list
        data = client.recv(1024).decode()
        new_peers = json.loads(data)

        # Add the new peers to the known peer list
        self.peers.update(new_peers)

        # Optionally, you could also send data to the server here
        # For example, sending your own peer list
        client.send(json.dumps(list(self.peers)).encode())

        # Close the client socket
        client.close()

# Example usage
if __name__ == "__main__":
    server = Server()
    host = "localhost"
    port = 5000
    server_thread = threading.Thread(target=server.run_server, args=(host, port))
    server_thread.start()

    # Optionally: connecting to another peer (you should know its host and port beforehand)
    # server.connect_to_peer("localhost", 6000)
