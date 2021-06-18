from pymongo import MongoClient, results


class Client:
    def __init__(self, password):
        cluster = MongoClient(f'mongodb+srv://mezgoodle:{password}@githubhelper.2tnee.mongodb.net/githubhelper'
                              '?retryWrites=true&w=majority')
        db = cluster['githubhelper']
        self.collection = db['tokens']

    def insert(self, data: dict) -> results.InsertOneResult:
        try:
            return self.collection.insert_one(data)
        except Exception as e:
            print('Error:', e)

    def get(self, query: dict) -> dict:
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print('Error:', e)

    def update(self, query: dict, data: dict) -> results.UpdateResult:
        try:
            return self.collection.update_one(query, {'$set': data})
        except Exception as e:
            print('Error:', e)

    def delete(self, query: dict) -> results.DeleteResult:
        try:
            return self.collection.delete_one(query)
        except Exception as e:
            print('Error:', e)

# client = Client('password')
# print(client.update({'token': "ghp_31eqweqw"}, {'$set': {'telegram_id': 'tg_test_id'}}))
