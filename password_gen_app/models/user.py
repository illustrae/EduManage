from password_gen_app.config.mysqlconnection import connectToMySQL
from password_gen_app import app
import re
from password_gen_app.models.password import Password
from cryptography.fernet import Fernet
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
    def create(cls, postData):
        pw_hash = bcrypt.generate_password_hash(postData['password'])
        data = {
            'first_name': postData['first_name'],
            'last_name': postData['last_name'],
            'email': postData['email'],
            'username': postData['username'],
            'password': pw_hash
        }
        query = 'INSERT INTO users (first_name, last_name, email, username, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s)'
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_one(cls,id):
        query = f'SELECT * FROM users WHERE ID = {id}'
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])
    
    @classmethod
    def user_with_passwords(cls, data):
        query = "SELECT * FROM users LEFT JOIN passwords ON users.id = passwords.users_id WHERE users.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        user_passwords = cls(result[0])
        if result[0]['keygen'] != None:
            for password in result:
                pass_gen=Fernet(password['keygen'])
                password['gen_password']= pass_gen.decrypt(password['gen_password']).decode()
                data = {
                "id": password['passwords.id'],
                "gen_password": password['gen_password'],
                "keygen": password['keygen'],
                "users_id": password['users_id'], 
                "created_at": password['created_at'],
                "updated_at": password['updated_at']
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
        print(query)
        return connectToMySQL(db).query_db(query, data)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @staticmethod
    def register_validator(postData):
        is_valid = True
        EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 3:
            flash("First name should be at least 3 characters.", 'register')
            is_valid = False 
        if len(postData['last_name']) < 3:
            flash("Last name should be at least 3 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(postData['email']):
            flash("Invalid email address format!", 'register')
            is_valid = False
        if len(postData['username']) <= 5:
            flash("Username should be at least 6 characters.", 'register')
            is_valid = False
        if  0 <= len(postData['password']) <= 7:
            flash("Password needs to be at least 8 characters.", 'register')
            is_valid = False
        elif postData['c_password'] != postData['password']:
            flash("Passwords do not match!", 'register')
            is_valid = False
        if is_valid:
            flash('Successfully registered!', 'register')
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