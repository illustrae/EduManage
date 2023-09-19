from password_gen_app import app
from flask import render_template, session, redirect, request
from cryptography.fernet import Fernet
from ..models.password import Password
from ..models.user import User



@app.route('/register')
def register_user():
    
    return render_template('register.html')

@app.route('/processregister', methods=['POST'])
def process_register():
    if User.registervalidator(request.form):
        session['user_logged_id']=User.create(request.form)
        return redirect('/logged_in')
    return redirect('/register')

@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/processlogin', methods=['POST'])
def process_login():
    if User.loginvalidator(request.form):
        return redirect('/logged_in')
    return redirect('/login')

@app.route('/account')
def user_account():
    return render_template('test.html', passwords=Password.get_all_passwords())