import csv
import os
from datetime import datetime

USERS_FILE = "Data/users.csv"
AUTH_LOG   = "Data/auth_log.csv"

#this will update the login report/record 
def _log_auth(action, username, detail):
    try:
        #this will check if the file exists
        exists = os.path.isfile(AUTH_LOG)
        with open(AUTH_LOG, "a", newline="") as f: #open Data/auth_log.csv then append the new line
            w = csv.writer(f) 

            if not exists: #this just check if we haven't create the file before, it just rewrite the header
                w.writerow(["timestamp", "action", "username", "detail"])
            #write the report of what just happened 
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, username, detail])
    except IOError:
        pass #ignore if error

def _load_users():
    users = {}
    if not os.path.isfile(USERS_FILE):
        return users
    try:
        with open(USERS_FILE, newline="") as f:
            for row in csv.DictReader(f):
                users[row["username"]] = row["password"]
    except IOError:
        pass
    return users

def _save_users(users: dict):
    os.makedirs("Data", exist_ok=True)
    with open(USERS_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["username", "password"])
        for uname, password in users.items():
            w.writerow([uname, password])
#for this function both username and password has to be a string and the return type is bool (True/False)
def register_user(username: str, password: str) -> bool:
    if len(password) < 6:
        print("  Password must be at least 6 characters.")
        return False
    #bring the existing username (if have any) to see if the name has already taken 
    users = _load_users()
    if username in users:
        print(f"  Username '{username}' is already taken.")
        return False
    #if the password is secured and the name is new then we can put the new username and password into the new dictionary 
    users[username] = password
    _save_users(users)
    _log_auth("REGISTER", username, "success")
    print(f"  Admin '{username}' registered successfully.")
    return True
#this will check if user enter the right username/password
def login(username, password):
    users = _load_users()
    if username not in users or users[username] != password:
        #if the inputs are incorrect then update the log in run _log_auth()
        _log_auth("LOGIN_FAIL", username, "invalid credentials")
        print("  Invalid username or password.")
        return None
    #if the inputs are correct then update the log in run _log_auth()
    _log_auth("LOGIN_OK", username, "success")
    print(f"  Welcome, {username}!")
    return {"username": username, "role": "admin"}

def change_password(username, old_password, new_password):
    users = _load_users()
    if username not in users:
        print("  User not found.")
        return False
    if users[username] != old_password:
        print("  Current password is incorrect.")
        _log_auth("PWD_CHANGE_FAIL", username)
        return False
    if len(new_password) < 6:
        print("  New password must be at least 6 characters.")
        return False

    users[username] = new_password
    _save_users(users)
    _log_auth("PWD_CHANGE_OK", username)
    print("  Password changed successfully.")
    return True

def default_admin():
    if not os.path.isfile(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        register_user("admin", "admin123")
        print("  Default credentials  —  username: admin | password: admin123")
        print("  Please change this password after first login.\n")

if __name__ == "__main__":
    pass
