#!/usr/bin/env python
from flask import Flask, jsonify, request
import segno
import pymongo
from wallet.core.utils.jprint import jprint  # noqa
from server import bitcoin
from models import Transaction

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
    if not q:
        return jsonify({"error": "q required"})

    # This is a pretty cvrude check...
    if len(q) < 64:
        address = mongo.bitcoin.addresses.find_one({"address": q}, {"_id": 0})
        address.update({"qrcode": create_qr_code(address)})
        return jsonify(address)
    else:
        return jsonify(Transaction(q).formated())


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
