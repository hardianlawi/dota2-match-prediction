import pymongo


class MongoDB(object):

    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017/')
        self._db = self._client['mydatabase']
        self.pro_matches = self._db['pro_matches']
        self.matches_data = self._db['matches_data']

    def pro_matches_col_exist(self):
        return 'pro_matches' in self._db.list_collection_names()

    def matches_data_col_exist(self):
        return 'matches_db' in self._db.list_collection_names()
