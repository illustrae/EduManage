from flask import Flask, request,session,render_template,redirect
from password_gen_app import app
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
    return redirect('/')

@app.route('/logged_in')
def logged_main():
    if 'generated_password' in session and 'user_logged_in' in session:
        generated_password = session['generated_password']
        return render_template('main_logged_in.html', generated_password = generated_password, user=User.get_one(session['user_logged_in']))
    else:
        return render_template('main_logged_in.html', user=User.get_one(session['user_logged_in']))