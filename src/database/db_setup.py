from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

class Database():
    def __init__(self) -> None:
        self.cluster = MongoClient(
            'mongodb+srv://' +
            os.environ.get('MONGO_USERNAME') +
            ':'+
            os.environ.get('MONGO_PASSWORD') +
            '@cluster0.kqvet.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
            )

        self.db = self.cluster.get_database('charity_app')

    def get_blockchain_collection(self):
        return self.db.get_collection('blockchain')
    
    def get_users_collection(self):
        return self.db.get_collection('users')
        

