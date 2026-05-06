import json
import os

FILE = "users.json"

def load_users():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True
    return False
