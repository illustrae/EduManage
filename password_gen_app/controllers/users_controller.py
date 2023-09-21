from password_gen_app import app
from flask import render_template, session, redirect, request
from ..models.user import User
from ..models.password import Password



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

@app.route('/profile/<int:id>')
def user_profile(id):
    if 'user_logged_id' not in session:
        return redirect('/logout')
    data = {"id": id}
    passwords = User.user_with_passwords(data)
    Password.get_all_passwords()
    
    return render_template('profile.html', passwords=passwords)

@app.route('/edit_account/<int:id>')
def edit_account(id):
    if 'user_logged_id' not in session:
        return redirect('/logout')
    user = User.get_one(id)
    return render_template('editAccount.html', user = user)

@app.route('/update_account', methods=['POST'] )
def update_account():
    if 'user_logged_id' not in session:
        return redirect('/logout')
    User.update_user_account(request.form, session['user_logged_id'])
    return redirect(f'/profile/{session["user_logged_id"]}')