from flask import Flask, request,session,render_template,redirect
from password_gen_app import app
from ..models.password import Password
from ..models.user import User


@app.route('/')
def index():
    if 'user_logged_id' in session:
        return redirect("/logged_in")
    
    if 'generated_password' in session:
        return render_template('main.html', generated_password = session['generated_password'])
    else:
        return render_template('main.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    
    if not Password.password_form_validator(request.form):
        if 'user_logged_id' in session:
            return redirect('/logged_in')
        else:
            return redirect('/')
    session['generated_password'] = Password.password_generator(request.form, request.form.getlist("params"))

    if 'user_logged_id' in session:
        Password.create_password()
        return redirect('/logged_in')
    
    return redirect('/')

@app.route('/logged_in')
def logged_main():
    if 'generated_password' in session and 'user_logged_id' in session:
        Password.create_password()
        session.pop('generated_password')
        generate_password = Password.get_last_password()
        return render_template('main_logged_in.html', generated_password = generate_password.gen_password, user=User.get_one({'id':session['user_logged_id']}))
    else:
        return render_template('main_logged_in.html', user=User.get_one({'id':session['user_logged_id']}))