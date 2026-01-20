"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from models.user import User

class UserMongoDAO:
    def __init__(self):
        try:
            env_path = ".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MONGODB_HOST", "mongo")
            db_port = int(os.getenv("MONGO_PORT", 27017))
            db_name = os.getenv("MONGO_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")
            if db_user and db_pass:
                mongo_uri = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
                self.client = MongoClient(mongo_uri)
            else:
                self.client = MongoClient(host=db_host, port=db_port)
            self.db = self.client[db_name]
            self.collection = self.db["users"]
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MongoDB """
        users = self.collection.find()
        return [User(str(user.get('_id')), user.get('name'), user.get('email')) for user in users]

    def insert(self, user):
        """ Insert given user into MongoDB """
        result = self.collection.insert_one({
            "name": user.name,
            "email": user.email
        })
        return str(result.inserted_id)

    def update(self, user):
        """ Update given user in MongoDB (with ObjectId conversion) """
        try:
            object_id = ObjectId(user.id)
        except Exception:
            object_id = user.id  # fallback if already ObjectId
        self.collection.update_one(
            {"_id": object_id},
            {"$set": {"name": user.name, "email": user.email}}
        )

    def delete(self, user_id):
        """ Delete user from MongoDB with given user ID (with ObjectId conversion) """
        try:
            object_id = ObjectId(user_id)
        except Exception:
            object_id = user_id  # fallback if already ObjectId
        self.collection.delete_one({"_id": object_id})

    def delete_all(self): #optional
        """ Empty users collection in MongoDB """
        self.collection.delete_many({})
        
    def close(self):
        self.client.close()
