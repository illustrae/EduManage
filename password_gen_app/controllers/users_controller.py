from password_gen_app import app
from flask import render_template, session, redirect, request
from cryptography.fernet import Fernet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    
    
    #Will place generate_pw(request.form) method when built.
    
    
    
    if 'user_logged_in' in session:
        key = Fernet.generate_key()
        pass_gen=Fernet(key)
        pass_gen.encrypt(request.form['gen_password'])
    
    return redirect('/')