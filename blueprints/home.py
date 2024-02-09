from flask import Blueprint, jsonify, request,render_template
from flask_jwt_extended import jwt_required
from databse import client,blocks_collection
from bson.json_util import dumps
from extensions import file_blockchain,network,pbft_instance


view_home = Blueprint('view_home',__name__)

@view_home.route('/home',methods=['GET'])
def home():
    return render_template('index.html')

@view_home.route('/admin_home')
@jwt_required()
def admin_home():

    return render_template('admin_home.html')

@view_home.route('/review_chain',methods=['GET'])
@jwt_required()
def review_chain():
    return render_template('review_chain.html')

@view_home.route('/add_diploma',methods=['GET'])
@jwt_required()
def add_diploma():
    return render_template('add_diploma.html')