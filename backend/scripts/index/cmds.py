from .group import index

import click
from server import bitcoin
from server import mongo
from wallet.core.utils.jprint import jprint
from models.transaction.model import Transaction


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

        hash = bitcoin.getblockhash(idx)
        block = bitcoin.getblock(hash)
        print(f"{idx} of {height} {block['hash']}  Transactions {len(block['tx'])}")
        for tx in block["tx"]:
            # tx = "5933f83f611896b3f35fd650b4f03f9d85d4b6491299c5c5398000834929a224"
            txn = Transaction(tx)
            # jprint(txn.tx)
            # jprint(txn.inputs)
            # jprint(txn.outputs)
            # input()

            for address in txn.outputs:
                # Update address collection
                mongo.bitcoin.addresses.update_one(
                    {"address": address["address"]},
                    {"$addToSet": {"inputs": tx}},
                    upsert=True,
                )
            for address in txn.inputs:
                mongo.bitcoin.addresses.update_one(
                    {"address": address["address"]},
                    {"$addToSet": {"outputs": tx}},
                    upsert=True,
                )

            if txn.errors:
                jprint(txn.errors)

        if idx and idx % 100 == 0:
            print("\nTotal addresses: %s" % len(addresses))
            print("Total txns: %s" % len(transactions))
