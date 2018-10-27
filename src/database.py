import pymongo


class MongoDB(object):

    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017/')
        self._db = self._client['mydatabase']
        self.pro_matches = self._db['pro_matches']
        self.matches_data = self._db['matches_data']

    def pro_matches_col_exist(self):
        return self._exist('pro_matches')

    def matches_data_col_exist(self):
        return self._exist('matches_data')

    def query_all_data(self, collection_name):
        """Create generator to iterate over the data from a collection

        Args:
            collection_name (str): the name of the collection to be queried

        Raises:
            CollectionNotFoundError: If the collection specified does not exist

        Returns:
            generator
        """

        if not self._exist(collection_name):
            raise CollectionNotFoundError('Collection does not exist.')
        print('Querying data from %s.' % collection_name)
        return self._query_from_collection(collection_name)

    def _exist(self, collection_name):
        return collection_name in self._db.list_collection_names()

    def _query_from_collection(self, collection_name):
        collection = self._db[collection_name]
        docs_generator = collection.find({})
        return docs_generator


class CollectionNotFoundError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
