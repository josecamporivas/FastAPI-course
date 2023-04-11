from pymongo import MongoClient

# For MongoDB database running in local
db_client = MongoClient().local # automatically connects to local instance of MongoDB

# For MongoDb database running in remote
# urlDatabase = '' # here copy the url database
# db_client = MongoClient(urlDatabase)