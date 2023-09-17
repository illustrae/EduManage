from password_gen_app import app
from flask import render_template, session, redirect, request
from cryptography.fernet import Fernet
from ..models.password import Password
@app.route('/')
def index():
    if 'generated_password' in session:
        generated_password = session['generated_password']
        return render_template('main.html', generated_password = generated_password)
    else:
        return render_template('main.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    print("I'm here")
    session['generated_password'] = Password.password_generator(request.form, request.form.getlist("params"))

    if 'user_logged_in' in session:
        key = Fernet.generate_key()
        pass_gen=Fernet(key)
        pass_gen.encrypt(request.form['gen_password'])
    
    return redirect('/')