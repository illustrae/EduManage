from password_gen_app import app
from password_gen_app.controllers import users_controller, passwords_controller
# from password_gen_app.tasks.tasks import start_password_timer
from flaskwebgui import FlaskUI, close_application
import pyautogui



if __name__ =='__main__':

     # FlaskUI(app=app, server="flask", width=800, height=500).run()
     app.run(debug=True)