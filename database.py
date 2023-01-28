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
        if user is not None:
            if check_password_hash(password=password, pwhash=user['password']):
                return True
            elif not check_password_hash(password=password, pwhash=user['password']):
                flash("Incorrect password")
                return False
        else:
            flash("username not found register instead")
            return "not_found"

    def save_image(self, data, path, name):

        for item in data:
            class_name = item[2:]
            class_score = data[item]['score']
            break
        user = self.users.find_one({
            'username': name
        })

        history = user['history']
        new_history = [{
            'name': class_name,
            'score': class_score,
            'path': path
        }]
        for item in history:
            new_history.append(item)
        self.users.update_one(
            {'username': name}, {"$set": {'history': new_history}}
        )

    def get_history(self, name):
        user = self.users.find_one({
            'username': name
        })
        user.get('history')
        return user.get('history')
