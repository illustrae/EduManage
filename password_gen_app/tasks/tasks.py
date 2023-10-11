
import schedule
from schedule import every, run_pending
import time

from ..models.password import Password
from ..controllers.passwords_controller import Password


stop_delete = False
has_deleted = False

def delete_password_timer():
    global has_deleted
    password_id = Password.get_all_passwords()
    print("Deleting passwords...")
    for pass_id in password_id:
        Password.delete_password(pass_id)
    has_deleted = True
#running the delete function every hour. Once deleted it should no longer delete.
schedule.every(1).hour.do(delete_password_timer)

def start_password_timer():
    global stop_delete
    while not stop_delete:
        if not has_deleted:
            schedule.run_pending()
            time.sleep(60)
        else:
            stop_password_timer()

def stop_password_timer():
    print("No longer run after passwords have been deleted..")
    global stop_delete
    stop_delete = True



    

