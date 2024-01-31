from flask_socketio import emit
from extensions import pool ,file_blockchain
import traceback


# Initialize your transaction pool and other necessary components here

def register_socketio_events(socketio):
    
    @socketio.on('connect')
    def handle_connect():
        emit('message', {'data': 'Connected'})

    @socketio.on('transaction')
    def handle_transaction(transaction):
        try:
            if 'pdf_data' not in transaction or 'pdf_name' not in transaction:
                raise ValueError("Invalid transaction format")

            pool.add_transaction_to_pool(transaction)

            emit('transaction', transaction, broadcast=True)

        except Exception as e:
            print(f"Error handling transaction: {e}")
            traceback.print_exc()

    @socketio.on('request_blockchain')
    def handle_request_blockchain():
        emit('response_blockchain', file_blockchain.to_dict())