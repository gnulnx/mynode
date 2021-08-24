#!/usr/bin/env python
from flask import Flask, jsonify, request
import segno
import pymongo
from wallet.core.utils.jprint import jprint  # noqa
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

        # address.tx_out = []
        # for txn in address["vouts"]:
        #     address.tx_out.append(bitcoin.getrawtransaction(tx, True))

        # Your qr codes don't match blockchain.com
        address.update(
            {
                "qr": create_qr_code(address["address"]),
                "data_type": "address",
                "tx_outs": [
                    bitcoin.getrawtransaction(tx, True) for tx in address["vouts"]
                ],
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
