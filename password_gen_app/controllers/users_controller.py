from password_gen_app import app
from flask import render_template, session, redirect, request
from ..models.user import User
from flask_socketio import SocketIO
socketio = SocketIO(app)

@app.route('/register')
def register_user():

    return render_template('register.html')

@app.route('/process_register', methods=['POST'])
def process_register():
    if User.register_validator(request.form):
        session['user_logged_id']=User.create(request.form)
        return redirect('/logged_in')
    return redirect('/register')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    if User.login_validator(request.form):
        return redirect('/logged_in')
    return redirect('/login')

@app.route('/profile/<int:id>')
def user_profile(id):
    if 'user_logged_id' not in session:
        return redirect('/logout')
    return render_template('profile.html', user=User.user_with_passwords({"id": id}),on_profile = True)

@app.route('/edit_account/<int:id>')
def edit_account(id):
    if 'user_logged_id' not in session:
        return redirect('/logout')
    return render_template('editAccount.html', user = User.get_one(id))

@app.route('/update_account', methods=['POST'] )
def update_account():
    if 'user_logged_id' not in session:
        return redirect('/logout')
    User.update_user_account(request.form)
    return redirect(f'/profile/{session["user_logged_id"]}')

@app.route("/delete_account/<int:id>")
def delete_account(id):
    if 'user_logged_id' not in session:
        return redirect('/logout')
    User.delete_user_account({"id": id})
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@socketio.on('disconnect')
def disconnect_user():
    session.pop('generated_password', None)
