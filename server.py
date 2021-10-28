from bitcoincli import Bitcoin
import pymongo
import json

# import bitcoin to use python based bitcoin-cli
bitcoin = Bitcoin("gnulnx", "bc", "localhost", 8334)

# import mongo to access mongo
mongo = pymongo.MongoClient(
    "mongodb://btc:utxo@localhost:27017", serverSelectionTimeoutMS=5000
)
try:
    mongo.server_info()
except Exception:
    print("Unable to connect to the server.")
