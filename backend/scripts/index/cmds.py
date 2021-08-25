from .group import index

import click
from server import bitcoin
from server import mongo
from wallet.core.utils.jprint import jprint
from models.transaction.model import Transaction
from datetime import datetime
from tqdm import tnrange, tqdm
from tqdm import tqdm
from alive_progress import alive_bar


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

    with alive_bar(height - start, bar="blocks", spinner="fish2", length=75) as bar:
        for idx in range(start, height):
            hash = bitcoin.getblockhash(idx)
            block = bitcoin.getblock(hash, 1)
            out = mongo.bitcoin.blocks.update_one(
                {"idx": idx},
                {
                    "$set": {
                        "nTx": block["nTx"],
                        "ts": datetime.fromtimestamp(block["time"]),
                        "hash": hash,
                    }
                },
                upsert=True,
            )
            bar()
            if out.matched_count == 1:
                # Don't process blocks that have already been processed
                continue

            # A different type of output
            # ts = datetime.fromtimestamp(block["time"]).strftime("%Y-%m-%d %h:%M:%S")
            # print(
            #     f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}"
            # )

            for tx in block["tx"]:
                # tx = "5933f83f611896b3f35fd650b4f03f9d85d4b6491299c5c5398000834929a224"
                txn = Transaction(tx)

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
                    # TODO Log this...
                    jprint(txn.errors)
