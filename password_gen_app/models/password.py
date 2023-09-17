from password_gen_app.config.mysqlconnection import connectToMySQL
from password_gen_app import app
from flask import flash
from random import randint, shuffle

db='password_generator_schema'

class Password:
    def __init__(self, data):
        self.id = data['id']
        self.gen_password = data['gen_password']
        self.key = data['key']
        self.creator = data['users_id']
    
    @classmethod
    def create_password(cls,data):
        query = 'INSERT INTO passwords (gen_password, key, users_id) VALUE( %(gen_password)s, %(key)s, %(users_id)s)'
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

    
    @staticmethod
    def create_character_list(param, character_list):
        import string
        """This function creates a list called character list which determines the characters needed for each category

        Args:
            param (string): param is each string value from the list generated from request.form checkbox values
            character_list (list): a list that is being built with each iteration of the for in password generator function also where it's declaration exist. 

        Returns:
            list of lists that contains strings
        """    
        
        if param == "special":
            character_list.append(list(string.punctuation))
        elif param =="number":
            character_list.append(list(string.digits))
        elif param =="lowercase":
            character_list.append(list(string.ascii_lowercase))
        else:
            character_list.append(list(string.ascii_uppercase))
        return character_list

    @staticmethod
    def populate_and_shuffle(values_list, character_list):
        """This is a function that takes in several lists and creates a new list of strings that form the generated password.   

        Args:
            values_list (list): This is a list that declared on line 86. The values in the list are the number of instances in each category of the params.  
            character_list (list): The finished and completed return value from create_character_list on line 14. 
            counter(integer): A count to keep track of when to iterate the character_list to access the new list of string values.
            
        Returns:
            password_generated(list): A list to store all values to make the generated password and joined as a single string value. 
        """    
        password_generated = []
        counter=0
        
        for index in range(len(values_list)):
            for each_instance in range(values_list[index]):
                random_index = randint(1,len(character_list[counter])-1)
                print("random index", random_index)
                password_generated.append(character_list[counter][random_index-1:random_index][0])
                print(character_list[counter])
                character_list[counter].pop(random_index-1)
                print(character_list[counter])
                print(password_generated)
                shuffle(password_generated)
            counter+=1
            print("Finished",password_generated)
        return "".join(password_generated)


    @staticmethod
    def password_generator(data,params_list):
        """This function is the top most function that builds determines the number of characters for each category and builds the generated passwords with the helper functions.

        Args:
            data (request.form): form data
            params_list (list): Values from the checkbox selections 

        Returns:
            string: generated password
        """    
        num_of_each={}
        character_list=[]
        
        if len(params_list) == 4:
            percentages =[.2,.2,.2,.4]
            for index,param in enumerate(params_list):
                num_of_each[param] = round(int(data['password_length']) * (percentages[index]))
                character_list=Password.create_character_list(param,character_list)
                
        elif len(params_list) == 3:
            percentages =[.3,.3,.4]
            for index,param in enumerate(params_list):
                num_of_each[param] = round(int(data['password_length']) * (percentages[index]))
                character_list=Password.create_character_list(param,character_list)
        else:
            percentages =[.4,.6]
            for index,param in enumerate(params_list):
                num_of_each[param] = round(int(data['password_length']) * (percentages[index]))
                character_list=Password.create_character_list(param,character_list)
        
        print(num_of_each)
        values_list =[num_of_each[key] for key in num_of_each]
        if sum(values_list) == int(data['password_length']):
            print("Equal", values_list)
            return Password.populate_and_shuffle(values_list,character_list) 
        elif sum(values_list) > int(data['password_length']):
            values_list[randint(0,2)]-=1
            print("value is greater",values_list)
            return Password.populate_and_shuffle(values_list,character_list)
        else:
            values_list[randint(0,2)]+=1
            print("value is less",values_list)
            return Password.populate_and_shuffle(values_list, character_list)
    
    
    
    
    
    
    
