from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client['blockchainpdf']
blocks_collection = db['blocks']
transaction_collection = db['transactions']
users= db['users']