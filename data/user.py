from flask_login import UserMixin
import os
from werkzeug.security import generate_password_hash
from databse import users
from flask_jwt_extended import create_access_token,create_refresh_token


class User(UserMixin):
    def __init__(self, username, password, email,refresh_token):
        self.username = username
        self.password = password 
        self.email = email
        self.refresh_token = refresh_token

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'refresh_token': self.refresh_token
        }
    
    def load_user(email):
        user = users.find_one({"email": email})
        if user:
            return User(username=user["username"], password=user["password"], email=user["email"], refresh_token=user["refresh_token"])
        return None

    def create_user(username, password, email):
        user = users.find_one({"_id": email})
        if user or users.find_one({"username": username}):
            return False

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email,refresh_token=refresh_token)
        users.insert_one(new_user.to_dict())

        
        return {'access_token': access_token, 'refresh_token': refresh_token}
        

   
    
    

    