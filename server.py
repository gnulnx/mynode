from bitcoincli import Bitcoin
import pymongo
import json
import os

# import bitcoin to use python based bitcoin-cli
bitcoin = Bitcoin(
    os.environ.get("BC_USERNAME", "gnulnx"),
    os.environ.get("BC_PASSWORD", "bc"),
    os.environ.get("BC_HOST", "bs"),
    os.environ.get("BC_PORT", 8332),
)
# bitcoin = Bitcoin("gnulnx", "bs", "localhost", 8332)

# import mongo to access mongo
mongo = pymongo.MongoClient(
    "mongodb://btc:utxo@localhost:27017", serverSelectionTimeoutMS=5000
)
try:
    mongo.server_info()
except Exception:
    print("Unable to connect to the server.")
