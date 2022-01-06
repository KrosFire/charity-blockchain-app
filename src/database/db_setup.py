from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

class DataBase():
    def __init__(self) -> None:
        self.cluster = MongoClient(
            'mongodb+srv://' +
            os.environ.get('MONGO_USERNAME') +
            ':'+
            os.environ.get('MONGO_PASSWORD') +
            '@cluster0.kqvet.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
            )

        self.db = self.cluster.get_database('charity_app')
        self.collection = self.db.get_collection('blockchain')
    
    def push_data(self, *data) -> None:
        self.collection.insert_many(data)
    
    def get_data(self, query: dict = {}) -> list[dict]:
        return self.collection.find(query)

