from notes_app.config.mysqlconnection import connectToMySQL
from notes_app import app, DATABASE
from notes_app.clients.s3 import S3Uploader
import re
from flask import flash

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.profile_img = data['profile_img']

    @classmethod
    def create_new_user(cls, data):
        query = '''
        INSERT INTO users (first_name, last_name, email, phone_number, password, profile_img)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(password)s, %(profile_img)s);
        '''
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    @classmethod
    def get_user(cls, data):
        query = '''
        SELECT * FROM users WHERE email = %(email)s
        '''

        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])

    @staticmethod
    def upload_img_s3(file_obj, user_info):
        s3 = S3Uploader()
        object_name = f"{user_info['first_name'].lower()}_{user_info['last_name'].lower()}_profile_img"
        s3.upload_fileobj(file_obj, object_name)
        return f"https://naprofileimgs.s3.amazonaws.com/{object_name}"

    @staticmethod
    def validate_new_user(user_info):

        is_valid = True

        if len(user_info['first_name']) < 2:
            flash('Please enter a valid name', 'first_name_err')
            is_valid = False
        if len(user_info['last_name']) < 2:
            flash('Please enter a valid last name', 'last_name_err')
            is_valid = False
        if not EMAIL_REGEX.match(user_info['email']):
            flash('Please use a valid email', 'email_regex_err')
            is_valid = False
        if User.get_user({'email': user_info['email']}):
            if user_info['email'] == User.get_user({'email': user_info['email']}).email:
                flash('Email is already registered', 'email_regex_err')
                is_valid = False
        if len(user_info['password']) < 8:
            flash('Password should be at least 8 characters long', 'short_password_err')
            is_valid = False
        # if not PASSWORD_REGEX.match(user_info['password']):
        #     flash('Password must contain one upper case letter, one number and one special character',
        #           'password_regex_err')
        #     is_valid = False
        if not bcrypt.check_password_hash(user_info['password'], user_info['confirm_password']):
            # user_info['password'] != user_info['confirm_password']:
            flash('Passwords do not match', 'password_match_err')
            is_valid = False
        # if not user_info['profile_img']:
        #     flash('Please upload a profile picture', 'profile_img_err')
        #     is_valid = False
        if len(user_info['phone_number']) < 10:
            flash('please enter a valid phone number', 'phone_number_err')
            is_valid = False

        return is_valid

    @classmethod
    def log_in_check(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results) == 0:
            print("email not found")
            flash("Wrong credentials, please try again ", "email_log_in_err")
            return False
        elif not bcrypt.check_password_hash(results[0]['password'], data['password']):
            print('wrong password')
            print(f"submitted: {data['password']}")
            print(f"actual: {results[0]['password']}, {results[0]['email']}")
            flash("Wrong credentials, please try again ", "pw_log_in_err")

            return False
        print('log in successful')
        return results[0]['id']


