from flask import Flask, request,session,render_template,redirect
from password_gen_app import app
from cryptography.fernet import Fernet
from ..models.password import Password
from ..models.user import User


@app.route('/')
def index():
    
    if 'generated_password' in session:
        generated_password = session['generated_password']
        return render_template('main.html', generated_password = generated_password)
    else:
        return render_template('main.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    session['generated_password'] = Password.password_generator(request.form, request.form.getlist("params"))

    if 'user_logged_id' in session:
        key = Fernet.generate_key().decode()
        pass_gen=Fernet(key)
        print("Generated Password", session['generated_password'])
        encrypted_pw=pass_gen.encrypt(session['generated_password'].encode())
        decrypted_pw = pass_gen.decrypt(encrypted_pw).decode()
        print(encrypted_pw)
        print(decrypted_pw)
        data ={
            'gen_password': pass_gen.encrypt(session['generated_password'].encode()),
            'keygen': key,
            'users_id': session['user_logged_id']
        }
        Password.create_password(data)
        return redirect('/logged_in')
    
    return redirect('/')

@app.route('/logged_in')
def logged_main():
    if 'generated_password' in session and 'user_logged_id' in session:
        generated_password = session['generated_password']
        
        return render_template('main_logged_in.html', generated_password = generated_password, user=User.get_one(session['user_logged_id']))
    else:
        return render_template('main_logged_in.html', user=User.get_one(session['user_logged_id']))