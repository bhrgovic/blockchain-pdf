from blueprints.transactions import transactions_blueprint
from blueprints.add_pdf import pdf_blueprint
from blueprints.login import login_blueprint
import atexit
from app import create_app
from utils.blockchain_utils import save_blockchain


        


if __name__ == '__main__':
    app = create_app()

    app.register_blueprint(transactions_blueprint)
    app.register_blueprint(pdf_blueprint)
    app.register_blueprint(login_blueprint)

    app.run(debug=True, host="0.0.0.0")
    
    atexit.register(save_blockchain)