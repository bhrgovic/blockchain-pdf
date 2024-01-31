from flask import Blueprint, jsonify, request, render_template,redirect,url_for
from bson.json_util import dumps
from extensions import file_blockchain,network,pbft_instance,login_manager
import traceback
import hashlib
from databse import users
from data.user import User
from flask_login import login_user
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token
from werkzeug.security import check_password_hash

login_blueprint = Blueprint('login_blueprint', __name__)

@login_blueprint.route("/home",methods=["GET"])
@jwt_required()
def home():
    return render_template('index.html')



@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        print(f"Received email: {email}")  # Print the received email
        print(f"Received password: {password}")  # Print the received password
        user = User.load_user(email)
        print(f"Loaded user: {user}")  # Print the loaded user
        if user:
            print(f"User password hash: {user.password}")  # Print the user's password hash
            print(f"Check password: {check_password_hash(user.password, password)}")  # Print the result of the password check
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid username/password'}, 401
    return render_template('login.html')

@login_blueprint.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username)
        user = User.create_user(username,password,email)
        if user is False:            
            return render_template('register.html', error_message='Registration failed, username or email already in use. Please try again.')
        else:
            return render_template('register.html', success_message='Registration successful! You can now login.')
    return render_template('register.html')

@login_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return {'access_token': new_token}
