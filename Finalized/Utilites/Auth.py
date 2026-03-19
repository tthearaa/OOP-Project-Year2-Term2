import csv
import os
from datetime import datetime

USERS_FILE = "Data/users.csv"
AUTH_LOG   = "Data/auth_log.csv"

def _log_auth(action, username, detail):
    try:
        exists = os.path.isfile(AUTH_LOG)
        with open(AUTH_LOG, "a", newline="") as f:
            w = csv.writer(f)
            if not exists:
                w.writerow(["timestamp", "action", "username", "detail"])
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, username, detail])
    except IOError:
        pass

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

def register_user(username: str, password: str) -> bool:
    if len(password) < 6:
        print("  Password must be at least 6 characters.")
        return False

    users = _load_users()
    if username in users:
        print(f"  Username '{username}' is already taken.")
        return False

    users[username] = password
    _save_users(users)
    _log_auth("REGISTER", username)
    print(f"  Admin '{username}' registered successfully.")
    return True

def login(username, password):
    users = _load_users()
    if username not in users or users[username] != password:
        _log_auth("LOGIN_FAIL", username)
        print("  Invalid username or password.")
        return None

    _log_auth("LOGIN_OK", username)
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
