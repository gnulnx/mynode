from scripts.mynode import mynode
import click
from server import bitcoin
from server import mongo
import json
import time
from backend.wallet.core.utils.jprint import jprint


@mynode.group()
def index():
    """
    Transaction/Address Indexing Stuff
    """


@index.command()
@click.option("--start", default=1, help="Start block")
def all(start):
    info = bitcoin.getblockchaininfo()
    # The total number of blocks on the node
    height = info["blocks"]

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
    print("height: %s" % height)
    print("start: %s" % start)

    for idx in range(start, height):
        # Track the unprocessable blocks so we don't have to do it again on each new iteration
        if mongo.bitcoin.badblocks.find_one({"blocks": idx}):
            continue

        if not idx or idx % 100 == 0:
            print(f"\n{idx} of {height}", end="", flush=True)
        else:
            print(".", end="", flush=True)

        hash = bitcoin.getblockhash(idx)
        block = bitcoin.getblock(hash)
        for tx in block["tx"]:
            txn = bitcoin.getrawtransaction(tx, True)

            if "error" in txn:
                # "The genesis block coinbase is not considered an ordinary transaction and cannot be retrieved"
                continue

            # Is coinbase transaction?  True/False
            # coinbase = any(["coinbase" in vin for vin in txn["vin"]])
            # txn_hex = txn["hex"]

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

                        # Update address collection
                        mongo.bitcoin.addresses.update_one(
                            {"address": address},
                            {"$addToSet": {"vouts": tx}},
                            upsert=True,
                        )
                        # Update transactions collection
                        mongo.bitcoin.transactions.update_one(
                            {"tx": tx},
                            {"$addToSet": {"vouts": address}},
                            upsert=True,
                        )
                else:
                    if "addresses" in scriptpubkey:
                        jprint(txn)
                        print(
                            "What Kind of transaction is this?  Is there an addresses section?"
                        )
                        input()
                    else:
                        # Write an entry to the badblocks collection so we don't try it again.
                        mongo.bitcoin.badblocks.update_one(
                            {"bad": 1},
                            {"$addToSet": {"blocks": idx}},
                            upsert=True,
                        )

        if idx and idx % 100 == 0:
            print("\nTotal addresses: %s" % len(addresses))
            print("Total txns: %s" % len(transactions))
