#!/usr/bin/env python
import click
from backend.server import bitcoin
from backend.server import mongo
import json
import time
from os import walk
import sys
from backend.wallet.core.utils.jprint import jprint

# print("HERE")


@click.command()
def idx_txn_add():
    info = bitcoin.getblockchaininfo()
    # The total number of blocks
    height = info["blocks"]
    # Change this to what you want
    START_BLOCK = 200000

    """
    address[address] = {
        "vins": [txn1, txn2, txn3],
        "vouts": [txn1, txn2, txn3]
    }
    """
    addresses = {}

    """
    transactions[tx] = {
        "vins": [add1, add2, add3],
        "vouts": [add1, add2, add3]
    }
    """
    transactions = {}
    print("You are here")
    print("height: %s" % height)
    print("START_BLOCK: %s" % START_BLOCK)

    for idx in range(START_BLOCK, height):
        # We track teh unprocessable blocks so we don't have to do it again on each new iteration
        resp = mongo.bitcoin.badblocks.find_one({"blocks": idx})
        if resp:
            continue
        # if idx > 800 and idx < 1000:
        #     continue

        if not idx or idx % 100 == 0:
            print(f"\n{idx} of {height}", end="", flush=True)
        else:
            print(".", end="", flush=True)
        # print(idx)
        hash = bitcoin.getblockhash(idx)
        block = bitcoin.getblock(hash)
        # jprint(block)
        # input()
        for tx in block["tx"]:
            # Remove this.  Test only
            # tx = "d176d4960a78b41971f9d19207b59af6584b16ef323de55e983aec0100000000"
            txn = bitcoin.getrawtransaction(tx, True)
            # jprint(txn)
            # input()

            if "error" in txn:
                # "The genesis block coinbase is not considered an ordinary transaction and cannot be retrieved"
                continue

            coinbase = any(["coinbase" in vin for vin in txn["vin"]])
            # txn_hex = txn["hex"]

            newAdd = False
            for out in txn["vout"]:
                scriptpubkey = out["scriptPubKey"]

                if scriptpubkey["type"] in [
                    "pubkeyhash",
                    "witness_v0_keyhash",
                    "witness_v0_scripthash",
                    "scripthash",
                ]:
                    for address in scriptpubkey["addresses"]:
                        if address not in addresses:
                            addresses[address] = {"vins": [], "vouts": []}

                        addresses[address]["vouts"].append(tx)

                        if tx not in transactions:
                            transactions[tx] = {"vins": [], "vouts": []}

                        transactions[tx]["vouts"].append(address)

                        newAdd = True

                        mongo.bitcoin.addresses.update_one(
                            {"address": address},
                            {
                                "$addToSet": {"vouts": tx},
                            },
                            upsert=True,
                        )
                        mongo.bitcoin.transactions.update_one(
                            {"tx": tx},
                            {
                                "$addToSet": {"vouts": address},
                            },
                            upsert=True,
                        )
                else:
                    if "addresses" in scriptpubkey:
                        jprint(txn)
                        print("Whats up")
                        input()
                    else:
                        mongo.bitcoin.badblocks.update_one(
                            {"bad": 1},
                            {
                                "$addToSet": {"blocks": idx},
                            },
                            upsert=True,
                        )
                        # print("Check mongo")
                        # input()
                    # else:
                    #     print("Notimplemented: %s" % scriptpubkey["type"])

        if idx and idx % 100 == 0:
            print("\nTotal addresses: %s" % len(addresses))
            print("Total txns: %s" % len(transactions))


if __name__ == "__main__":
    idx_txn_add()
