from sys import hash_info
from .group import index
from bitcoincli import Bitcoin

import click

# from server import bitcoin
from pymongo import IndexModel, ASCENDING
from server import mongo
from wallet.core.utils.jprint import jprint
from models.transaction.model import Transaction
from datetime import datetime
from tqdm import tnrange, tqdm
from tqdm import tqdm
from alive_progress import alive_bar


@index.command()
@click.option("--start", default=0, type=int, help="Start block")
@click.option("--perf", default=0, type=bool, help="Start block")
@click.option(
    "--bitcoin-host",
    default="",
    type=str,
    help="The host for the Bitcoin server you will fetch/process data from",
)
@click.option(
    "--bitcoin-user",
    default="",
    type=str,
    help="The RPC user name for your Bitcoin server",
)
@click.option(
    "--bitcoin-password",
    default="",
    type=str,
    help="The RPC password for your Bitcoin server",
)
@click.option(
    "--bitcoin-port",
    default=8332,
    type=int,
    help="The RPC port for your Bitcoin server",
)
@click.option(
    "--queues",
    default=0,
    type=bool,
    help="Build the bitcoin.blockqueue collection and populate it",
)
def all(
    start, perf, bitcoin_host, bitcoin_user, bitcoin_password, bitcoin_port, queues
):
    # print("bitcoin_user: %s" % bitcoin_user)
    # print("bitcoin_password: %s" % bitcoin_password)
    # print("bitcoin_host: %s" % bitcoin_host)
    # print("bitcoin_port: %s" % bitcoin_port)
    # input()
    # bitcoin = Bitcoin("gnulnx", "bc", "bs", 8332)
    bitcoin = Bitcoin(
        bitcoin_user,
        bitcoin_password,
        bitcoin_host,
        bitcoin_port,
    )
    info = bitcoin.getblockchaininfo()
    # The total number of blocks on the node
    height = int(info["blocks"])
    print(height)
    # Build the mongo queue database

    if queues:
        curr_blocks = [
            i["idx"] for i in mongo.bitcoin.blocks.find({}, {"_id": 0, "idx": 1})
        ]
        print(f"Current # of block idx {len(curr_blocks)}")

        curr_queues = [i["i"] for i in mongo.bitcoin.queue.find({}, {"_id": 0, "i": 1})]
        print(f"Current # of queues with idx {len(curr_queues)}")

        items_to_insert = set(range(height)) - set(curr_blocks) - set(curr_queues)
        print(f"Total items to insert to queue: {len(items_to_insert)}")

        if items_to_insert:
            add_index = IndexModel([("status", ASCENDING)])
            mongo.bitcoin.queue.create_indexes([add_index])
            mongo.bitcoin.queue.insert_many(
                [{"i": i, "status": 0} for i in items_to_insert]
            )

    # print("done")
    # input()

    MONGO = True
    if perf == True:
        MONGO = False

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

    """
    Create indexes for the mongo collections
    """
    idx_index = IndexModel([("idx", ASCENDING)])
    hash_index = IndexModel([("hash", ASCENDING)])
    mongo.bitcoin.blocks.create_indexes([idx_index, hash_index])

    add_index = IndexModel([("address", ASCENDING)])
    mongo.bitcoin.addresses.create_indexes([add_index])

    print("height: %s" % height)
    print("start: %s" % start)

    # If we pass in start use that as block id x start.
    # Otherwise look at blocks collection and start 1 past the last processed idx
    if not start and MONGO:
        out = list(
            mongo.bitcoin.blocks.aggregate(
                [{"$group": {"_id": "max", "max_idx": {"$max": "$idx"}}}]
            )
        )
        # If you add block sequentially then you can restart at last block
        start = out[0]["max_idx"] + 1 if out else 0
        print("Start block set from mongo at: %s" % start)

    # with alive_bar(height - start, bar="blocks", spinner="fish2", length=75) as bar:
    # for count, idx in enumerate(range(start, height)):
    # while q == bitcoin.queue.find_one():
    while q := mongo.bitcoin.queue.find_one_and_update(
        {"status": 0}, {"$set": {"status": 1}}
    ):

        idx = q["i"]
        _id = q["_id"]
        # if perf and count == 10:
        #     return

        if MONGO:
            out = list(mongo.bitcoin.blocks.find({"idx": idx}, {"idx": 1, "_id": 0}))
            block_processed = len(list(out)) > 0
            if block_processed:
                mongo.bitcoin.queue.delete_one({"_id": _id})
                # print(len(list(out)) > 0)
                print(f"Already processed block {idx} - {list(out)}")
                # input()
                continue

        # TODO REMOVE THIS LINE
        # idx = 151808
        hash = bitcoin.getblockhash(idx)
        block = bitcoin.getblock(hash, 2)

        # A different type of output
        ts = datetime.fromtimestamp(block["time"]).strftime("%Y-%m-%d %h:%M:%S")

        if MONGO:
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

        # bar()

        if MONGO and out.matched_count == 1:
            # Don't process blocks that have already been processed
            print(
                f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}, skip=True"
            )
            continue

        print(
            f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}"
        )

        for tx in block["tx"]:
            if perf:
                tx = "5933f83f611896b3f35fd650b4f03f9d85d4b6491299c5c5398000834929a224"

            # txn = Transaction(txid=tx)
            txn = Transaction(tx=tx)
            # input()

            if MONGO:
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

        # print("deleting: %s" % _id)
        # input()
        mongo.bitcoin.queue.delete_one({"_id": _id})
        # print("Check")
        # input()
