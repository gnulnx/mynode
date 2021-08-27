from bitcoincli import Bitcoin
import pymongo
import os

# import bitcoin to use python based bitcoin-cli
# bitcoin = Bitcoin("gnulnx", "bc", "bs", 8332)
bitcoin = Bitcoin(
    os.environ.get("BC_USERNAME", "gnulnx"),
    os.environ.get("BC_PASSWORD", "bc"),
    os.environ.get("BC_HOST", "localhost"),
    8332,
)
# print(bitcoin.getblockchaininfo())

# import mongo to access mongo
mongo = pymongo.MongoClient(
    "mongodb://btc:utxo@localhost:27017", serverSelectionTimeoutMS=5000
)
try:
    mongo.server_info()
except Exception:
    print("Unable to connect to mongo server.")
