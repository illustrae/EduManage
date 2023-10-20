from password_gen_app.config.mysqlconnection import connectToMySQL
from password_gen_app import app
import re
from password_gen_app.models.password import Password
from flask import flash,session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db='password_generator_schema'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.generated_passwords = []

    @classmethod
    def create(cls, data):
        postData = {}
        postData |= data
        postData['password'] = bcrypt.generate_password_hash(postData['password'])
        query = 'INSERT INTO users (first_name, last_name, email, username, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s)'
        return connectToMySQL(db).query_db(query,postData)
    
    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE ID = %(id)s'
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def user_with_passwords(cls, data):
        query = "SELECT * FROM users LEFT JOIN passwords ON users.id = passwords.users_id WHERE users.id = %(id)s ORDER BY passwords.created_at desc;"
        result = Password.decode_password(connectToMySQL(db).query_db(query, data))
        user_passwords = cls(result[0])
        if result[0]['keygen'] == None:
            return user_passwords
        for password in result:
            data = {
            "id": password['passwords.id'],
            "gen_password": password['gen_password'],
            "keygen": password['keygen'],
            "users_id": password['users_id'], 
            "created_at": password['passwords.created_at'],
            "updated_at": password['passwords.updated_at']
            }
            user_passwords.generated_passwords.append(Password(data))
        return user_passwords
    
    @classmethod
    def update_user_account(cls, post_data):
        data = { "id": session['user_logged_id']}
        data |= post_data
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, username=%(username)s WHERE id=%(id)s"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete_user_account(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(db).query_db(query, data)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @classmethod
    def if_user_info_exist(cls,key, data):
        query = f'''SELECT * FROM users 
        WHERE {key} = %(email)s;'''
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def profile_validator(postData):
        is_valid = True
        if 'first_name' in postData:
            EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            
            if len(postData['first_name']) < 3:
                flash("First name should be at least 3 characters.", 'register')
                is_valid = False 
            if len(postData['first_name']) > 75:
                flash("First name should be 75 characters or less.", 'register')
                is_valid = False 
            if len(postData['last_name']) < 3:
                flash("Last name should be at least 3 characters.", 'register')
                is_valid = False
            if len(postData['last_name']) > 75:
                flash("Last name should be 75 characters or less.", 'register')
                is_valid = False
            # email_exist=User.if_user_info_exist('email',{'email':postData['email']})
            if not EMAIL_REGEX.match(postData['email']):
                flash("Invalid email address format!", 'register')
                is_valid = False
            elif len(postData['email']) > 255:
                flash("Please shorten your email or try another email!", 'register')
                is_valid = False
            # elif not email_exist:
            #     flash("Email already taken.", 'register')
            #     is_valid = False
            # username_exist=User.if_user_info_exist('username',{'username': postData['username']})
            if len(postData['username']) <= 5:
                flash("Username should be at least 6 characters.", 'register')
                is_valid = False
            elif len(postData['username']) > 25:
                flash("Username should be 25 characters or less.", 'register')
                is_valid = False
            # elif not username_exist:
            #     flash("Username already taken.", 'register')
            #     is_valid = False
            if is_valid:
                flash("Profile Successfully Changed!", 'register')
        if 'password' in postData:
            if  0 <= len(postData['password']) <= 7:
                flash("Password needs to be at least 8 characters.", 'register')
                is_valid = False
            elif len(postData['password']) > 90:
                flash("Password needs to be 90 characters or less.", 'register')
                is_valid = False
            elif postData['c_password'] != postData['password']:
                flash("Passwords do not match!", 'register')
                is_valid = False
            
        return is_valid
    
    @staticmethod
    def login_validator(postData):
        is_valid = True
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL(db).query_db(query,postData)
        if len(result) < 1:
            is_valid = False
            flash("Username/Password doesn't match.", "login")
            return is_valid
        else:
            user = result[0]
        if not bcrypt.check_password_hash(user['password'], postData['password']):
            is_valid = False
            flash("Username/Password doesn't match.", "login")
            return is_valid
        session['user_logged_id']= user['id']
        return is_valid
    
    @staticmethod
    def password_validator(postData):
        is_valid = True
        if 'new_password' in postData:
            if postData['old_password'] == '':
                flash("Please input your current password.", "profile")
                is_valid = False
            if postData['new_password'] == '':
                flash("Please input your new password.", "profile")
                is_valid = False
            elif len(postData['new_password']) < 7:
                flash("New password needs to be 8 characters or more.", "profile")
                is_valid = False
            user = User.get_one({'id':session['user_logged_id']})
            if not bcrypt.check_password_hash(user.password, postData['old_password']):
                is_valid = False
                flash("Please verify your information is correct.", "profile")
                return is_valid
            elif len(postData['new_password']) > 90:
                print(len(postData['new_password']))
                flash("Password needs to be 90 characters or less.", 'profile')
                is_valid = False
            elif postData['c_password'] != postData['new_password']:
                flash("Passwords do not match!", 'profile')
                is_valid = False
            if is_valid:
                flash("Password Successfully Changed!", 'profile')
                data={
                    'password': bcrypt.generate_password_hash(postData['new_password']),
                    'id': session['user_logged_id']
                    }
                query = 'UPDATE users SET password = %(password)s WHERE id = %(id)s'
                connectToMySQL(db).query_db(query,data)
        return is_valid