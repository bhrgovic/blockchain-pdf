from flask import Flask, request, jsonify,Blueprint

view_master = Blueprint('view_master',__name__)

peers = set()

@view_master.route('/register_node', methods=['POST'])
def register():
    # Expected data format: {"address": "127.0.0.1", "port": 5001}
    print("Someone connected")
    data = request.get_json()
    address = data['address']
    port = data['port']
    peers.add((address, port))
    return jsonify(success=True), 200

@view_master.route('/nodes')
def get_nodes():
    print(jsonify(list(peers)))
    return jsonify(list(peers))