from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('menkos_db').query_db(query, data)

        if len(result) > 0:
            current_user = cls(result[0])
            return current_user
        else:
            return None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , password) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s );"
        results = connectToMySQL('menkos_db').query_db(query, data)
        return results

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if data['first_name'] == "":
            flash("First name is required", "error_registration_first_name")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", "error_registration_first_name")
            is_valid = False
        if data['last_name'] == "":
            flash("Last name is required", "error_registration_last_name")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "error_registration_last_name")
            is_valid = False
        if data['email'] == "":
            flash("Email is required", "error_registration_email")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_registration_email")
            is_valid = False
        if data['password'] == "":
            flash("Password is required", "error_registration_password")
            is_valid = False
        if data['confirm_password'] == "":
            flash("Confirm password is required", "error_registration_confirm_password")
            is_valid = False
        if data['confirm_password'] != data["password"]:
            flash("Password did not match confirm password.", "error_registration_confirm_password")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if data['email'] == "":
            flash("Email is required", "error_email_login_info")
            is_valid = False
        if data['password'] == "":
            flash("Password is required", "error_password_login_info")
            is_valid = False
        return is_valid
