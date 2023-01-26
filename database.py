import os
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from numpy import asarray
from PIL import Image
import blosc

from flask import flash

load_dotenv()
mongo_url = os.getenv('MONGODB')


class Users:
    def __init__(self):
        client = MongoClient(mongo_url)
        self.db = client['abdoDB']
        self.users = self.db['users']

    def register_user(self, username, email, password):

        user = self.users.find_one({'username': username})
        if user:
            flash("Username already exists!!")
            return False

        self.users.insert_one({
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'history': []
        })
        return True

    def login_user(self, name, password):
        user = self.users.find_one({
            'username': name
        })
        if user:
            if check_password_hash(password=password, pwhash=user['password']):
                return True
            else:
                flash("incorrect password")
                return False

    def save_image(self, path, name):

        print(path)
        user = self.users.find_one({
            'username': name
        })
        history = user['history']
        new_history = [path]
        for src in history:
            new_history.append(src)
        self.users.update_one(
            {'username': name}, {"$set": {'history': new_history}}
        )

    def get_history(self, name):
        print(name)
        user = self.users.find_one({
            'username': name
        })
        print(user)
        user.get('history')
        print(user.get('history'))
        return user.get('history')
