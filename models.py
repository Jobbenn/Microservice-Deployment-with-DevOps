# models.py
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson import ObjectId

mongo = PyMongo()

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.email = user_doc['email']

def get_user_by_email(email):
    user_doc = mongo.db.users.find_one({"email": email})
    return User(user_doc) if user_doc else None

def verify_user(email, password):
    user_doc = mongo.db.users.find_one({"email": email})
    if user_doc and check_password_hash(user_doc['password'], password):
        return User(user_doc)
    return None

def create_user(email, password):
    hashed = generate_password_hash(password)
    user_id = mongo.db.users.insert_one({"email": email, "password": hashed, "kanban": {"todo": [], "in_progress": [], "completed": []}}).inserted_id
    return str(user_id)

def get_user_kanban(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return user.get("kanban", {"todo": [], "in_progress": [], "completed": []})

def get_user_by_id(user_id):
    from bson import ObjectId
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_doc) if user_doc else None

def add_task_to_user(user_id, task):
    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"kanban.todo": task}}
    )

def move_task_for_user(user_id, task, from_section, to_section):
    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {f"kanban.{from_section}": task}}
    )
    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {f"kanban.{to_section}": task}}
    )
