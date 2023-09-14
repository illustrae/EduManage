from password_gen_app.config.mysqlconnection import connectToMySQL
from password_gen_app import app
from flask import flash

db='password_generator_schema'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.gen_password = data['gen_password']
        self.creator = data['users_id']
    
    @classmethod
    def create_password(cls,data, users_id):
        query = f'INSERT INTO passwords (gen_password, users_id) VALUE( %(gen_password)s, {users_id})'
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all_passwords(cls):
        query = 'SELECT * FROM passwords'
        results = connectToMySQL(db).query_db(query)
        passwords = [cls(row) for row in results]
        return passwords
    
    @classmethod
    def get_one_password(cls,id):
        query = f'SELECT * FROM passwords WHERE ID = {id}'
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])
    
    
    @classmethod
    def destroy(cls, id):
        query = f'SELECT * FROM passwords WHERE ID = {id}'
        return connectToMySQL(db).query_db(query)
    
    
    
    
    
    
