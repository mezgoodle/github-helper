from pymongo import MongoClient


class Client:
    def __init__(self):
        cluster = MongoClient('mongodb+srv://mezgoodle:<password>@githubhelper.2tnee.mongodb.net/githubhelper'
                              '?retryWrites=true&w=majority')
        db = cluster['githubhelper']
        self.collection = db['tokens']

    def insert(self, data: dict):
        self.collection.insert_one(data)

# token = {'token': 'ghp_31eqweqw', 'telegram_id': 'test_id'}
# collection.insert_one(token)
