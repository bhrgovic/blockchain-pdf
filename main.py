from blueprints.transactions import transactions_blueprint
from blueprints.add_pdf import pdf_blueprint
from blueprints.login import login_blueprint
from blueprints.home import view_home
from blueprints.master_point import view_master
from blueprints.pbft import view_pbft
from app import create_app
from extensions import network,pbft_instance,file_blockchain
import argparse
import requests
import databse



parser = argparse.ArgumentParser(description='Run a PBFT node.')
parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask app on.')
parser.add_argument('--node-id', type=int, required=True, help='ID of the PBFT node.')

args = parser.parse_args()        

def register_with_master(master_address, node_address, node_port):
    url = f"http://{master_address}/register_node"
    data = {"address": node_address, "port": node_port}
    nodeurl= str(node_address) + ":" + str(node_port)
    network.register_peer(nodeurl)
    requests.post(url, json=data)

def get_peers(master_address):
    response = requests.get(f"http://{master_address}/nodes")
    return response.json()

if __name__ == '__main__':
    
    app = create_app()

    master_node_address = "127.0.0.1:5000"
    my_address = "127.0.0.1"
    my_port = args.port

    if my_port != 5000:
        print("IM NOT MASTER NODE")
        register_with_master(master_node_address, my_address, my_port)
        peers = get_peers(master_node_address)
        # Update peers in the network
        for peer in peers:
            network.register_peer(peer)
        # Now update the total_nodes in PBFT instance

    pbft_instance.update_total_nodes(len(network.peers))

    app.register_blueprint(view_home)
    app.register_blueprint(transactions_blueprint)
    app.register_blueprint(pdf_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(view_master)
    app.register_blueprint(view_pbft)

    
    app.run(debug=True, host="0.0.0.0",port=my_port)