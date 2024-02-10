from pymongo import MongoClient
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO"))
db = client['blockchainpdf']
blocks_collection = db['blocks']
users= db['users']