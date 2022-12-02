import requests
import base64
import os
from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re
from flask_app.models.model_user import User
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Menko:
    def __init__(self, data):
        self.id = data['id']
        self.set_name = data['set_name']
        self.year = data['year']
        self.type = data['type']
        self.description = data['description']
        self.img_front = data['img_front']
        self.img_back = data['img_back']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO menkos ( set_name , year , type, description, img_front, img_back, user_id ) VALUES ( %(set_name)s , %(year)s , %(type)s , %(description)s, %(img_front)s, %(img_back)s, %(user_id)s);"
        return connectToMySQL('menkos_db').query_db(query, data)

    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM menkos JOIN users ON menkos.user_id = users.id"
        results = connectToMySQL('menkos_db').query_db(query)
        menkos = []
        for row in results:
            current_menko = (cls(row))
            user_data = {
                **row,
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at'],
                "id": row['users.id']
            }
            current_user = User(user_data)
            current_menko.user = current_user
            menkos.append(current_menko)
        return menkos

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM menkos JOIN users ON menkos.user_id = users.id WHERE menkos.id = %(id)s"
        result = connectToMySQL('menkos_db').query_db(query, data)

        if len(result) > 0:
            current_menko = cls(result[0])
            user_data = {
                **result[0],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at'],
                "id": result[0]['users.id']
            }
            current_menko.user = User(user_data)
            return current_menko
        else:
            return None

    @classmethod
    def update_one(cls, data):
        query = "UPDATE menkos SET set_name = %(set_name)s, year = %(year)s, type = %(type)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL('menkos_db').query_db(query, data)

    @classmethod
    def update_one_photo_front(cls, data):
        query = "UPDATE menkos SET img_front = %(img_front)s WHERE id = %(id)s;"
        return connectToMySQL('menkos_db').query_db(query, data)
    
    @classmethod
    def update_one_photo_back(cls, data):
        query = "UPDATE menkos SET img_back = %(img_back)s WHERE id = %(id)s;"
        return connectToMySQL('menkos_db').query_db(query, data)

    @classmethod
    def delete_one_menko(cls, data):
        query = "DELETE from menkos WHERE id = %(id)s;"
        return connectToMySQL('menkos_db').query_db(query, data)


    @staticmethod
    def get_pic_url(data):
        key = os.environ.get("IMGBB_KEY")
        url = "https://api.imgbb.com/1/upload"
        base_64 = base64.b64encode(data.read())
        payload = {
            "key": key,
            "image": base_64,
        }
        res = requests.post(url, payload)
        res = res.json()
        return res

    @staticmethod
    def validate_menko(data):
        is_valid = True
        if data['set_name'] == "":
            flash("Set name is required", "error_menko_set_name")
            is_valid = False
        if data['year'] == "":
            flash("Year is required", "error_menko_year")
            is_valid = False
        if data['type'] == "":
            flash("Type is required", "error_menko_type")
            is_valid = False
        if data['description'] == "":
            flash("Description is required", "error_menko_description")
            is_valid = False
        return is_valid
