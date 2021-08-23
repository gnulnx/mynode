#!/usr/bin/env python
# flask_web/app.py

from flask import Flask, jsonify, request
import pymongo
import segno
from wallet.core.utils.wallet import compute_wif
from wallet.core.utils.jprint import jprint
from server import bitcoin

app = Flask(__name__)

mongo = pymongo.MongoClient(
    "mongodb://btc:utxo@mongo:27017", serverSelectionTimeoutMS=5000
)


def create_qr_code(address, output="wallet_qr.png"):
    print("create_qr_code: %s" % address)
    qr = segno.make(address)
    return qr.svg_data_uri()


@app.route("/", methods=["GET"])
def main(q=None):
    q = request.args.get("q")
    if len(q) < 64:
        address = mongo.bitcoin.addresses.find_one({"address": q}, {"_id": 0})

        # Your qr codes don't match blockchain.com
        # wif = compute_wif(address["address"], compressed=True)
        address.update(
            {
                "qr": create_qr_code(address["address"]),
                "data_type": "address",
            }
        )
        return jsonify(address)
    else:
        txn = bitcoin.getrawtransaction(q, True)
        txn.update(
            {
                "data_type": "txn",
                "coinbase": any(["coinbase" in vin for vin in txn.get("vin", [])]),
            }
        )
        return jsonify(txn)


@app.route("/info", methods=["GET"])
def info():
    return jsonify(
        {
            "blockchain": bitcoin.getblockchaininfo(),
            "network": bitcoin.getnetworkinfo(),
            "memory": bitcoin.getmemoryinfo(),
            "mempool": bitcoin.getmempoolinfo(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
