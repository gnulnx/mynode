from sys import hash_info
from .group import index
from bitcoincli import Bitcoin
import time

import click

# from server import bitcoin
from pymongo import IndexModel, ASCENDING, InsertOne, DeleteOne, UpdateOne
from server import mongo
from wallet.core.utils.jprint import jprint
from models import Block, Transaction
from datetime import datetime
from tqdm import tnrange, tqdm
from tqdm import tqdm
from alive_progress import alive_bar


@index.command()
@click.option("--start", default=0, type=int, help="Start block")
@click.option(
    "--rpchost",
    default="",
    type=str,
    help="The host for the Bitcoin server you will fetch/process data from",
)
@click.option(
    "--rpcuser",
    default="",
    type=str,
    help="The RPC user name for your Bitcoin server",
)
@click.option(
    "--rpcpassword",
    default="",
    type=str,
    help="The RPC password for your Bitcoin server",
)
@click.option(
    "--rpcport",
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
def all(start, rpchost, rpcuser, rpcpassword, rpcport, queues):

    # Initilize our bitcoin client
    bitcoin = Bitcoin(rpcuser, rpcpassword, rpchost, rpcport)

    info = bitcoin.getblockchaininfo()

    # The total number of blocks on the node
    height = int(info["blocks"])
    print(height)

    if queues:
        # Build the mongo queue database
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
    if not start:
        out = list(
            mongo.bitcoin.blocks.aggregate(
                [{"$group": {"_id": "max", "max_idx": {"$max": "$idx"}}}]
            )
        )
        # If you add block sequentially then you can restart at last block
        start = out[0]["max_idx"] + 1 if out else 0
        print("Start block set from mongo at: %s" % start)

    # with alive_bar(height - start, bar="blocks", spinner="fish2", length=75) as bar:
    global_tracker = 0
    count = 0
    start_time = time.time()
    while q := mongo.bitcoin.queue.find_one_and_update(
        {"status": 0}, {"$set": {"status": 1}}
    ):

        # Perf test only
        # if count == 50:
        #     end_time = time.time()
        #     print(f"Elapsed time: {end_time - start_time}")
        #     return
        # count += 1

        idx = q["i"]
        _id = q["_id"]

        out = list(mongo.bitcoin.blocks.find({"idx": idx}, {"idx": 1, "_id": 0}))
        block_processed = len(list(out)) > 0
        if block_processed:
            mongo.bitcoin.queue.delete_one({"_id": _id})
            print(f"Already processed block {idx} - {list(out)}")
            continue

        hash = bitcoin.getblockhash(idx)
        block = bitcoin.getblock(hash, 2)

        # A different type of output
        ts = datetime.fromtimestamp(block["time"]).strftime("%Y-%m-%d %h:%M:%S")

        block_update = mongo.bitcoin.blocks.update_one(
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

        if block_update.matched_count == 1:
            # Don't process blocks that have already been processed
            print(
                f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}, skip=True"
            )
            continue

        start = time.time()

        if global_tracker == 0:
            global_txn_start = time.time()
            txn_start_count = mongo.bitcoin.transactions.count()

        add_requests = []
        for tx in block["tx"]:
            # tx = "5933f83f611896b3f35fd650b4f03f9d85d4b6491299c5c5398000834929a224"

            txn = Transaction(tx=tx, bitcoin_server=bitcoin)

            # jprint(txn.inputs)
            # jprint(txn.outputs)
            # input()

            txn_insert = mongo.bitcoin.transactions.insert_one(
                {
                    "txid": txn.txid,
                    "block": hash,
                    "inputs": txn.inputs,
                    "outputs": txn.outputs,
                    "coinbase": txn.coinbase,
                    "fee": txn.fee,
                }
            )
            txn_id = txn_insert.inserted_id

            try:
                for address in txn.outputs:
                    add_requests.append(
                        UpdateOne(
                            {"address": address["address"]},
                            {"$addToSet": {"inputs": txn_id}},
                            upsert=True,
                        )
                    )

                for address in txn.inputs:
                    add_requests.append(
                        UpdateOne(
                            {"address": address["address"]},
                            {"$addToSet": {"outputs": txn_id}},
                            upsert=True,
                        )
                    )

            except Exception as e:
                print(str(e))
                print("Address: %s" % address)
                print(tx["txid"])
                input()

            if txn.errors:
                # TODO Log this...
                jprint(txn.errors)

        # if len(add_requests) > 2000:
        #     mongo.bitcoin.addresses.bulk_write(add_requests)
        #     add_requests = []

        mongo.bitcoin.addresses.bulk_write(add_requests)
        mongo.bitcoin.queue.delete_one({"_id": _id})

        if global_tracker == 10:
            txn_end_count = mongo.bitcoin.transactions.count()
            global_txn_end = time.time()
            global_txn_per_s = (txn_end_count - txn_start_count) / (
                global_txn_end - global_txn_start
            )
            global_tracker = 0
        else:
            global_tracker += 1
            global_txn_per_s = None

        end = time.time()

        txn_per_s = len(block["tx"]) / (end - start)

        if global_txn_per_s:
            print(
                f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}, txns/s: {txn_per_s:.2f}s - {global_txn_per_s:.2f}s"
            )
        else:
            print(
                f"{idx} of {height}, hash: {block['hash']}, Transaction: {block['nTx']}, ts: {ts}, txns/s: {txn_per_s:.2f}s"
            )
        # print("Check")
        # input()


# @click.option("--start", default=0, type=int, help="Start block")
# @click.option(
#     "--rpchost",
#     default="",
#     type=str,
#     help="The host for the Bitcoin server you will fetch/process data from",
# )
# @click.option(
#     "--rpcuser",
#     default="",
#     type=str,
#     help="The RPC user name for your Bitcoin server",
# )
# @click.option(
#     "--rpcpassword",
#     default="",
#     type=str,
#     help="The RPC password for your Bitcoin server",
# )
# @click.option(
#     "--rpcport",
#     default=8332,
#     type=int,
#     help="The RPC port for your Bitcoin server",
# )
# @click.option(
#     "--queues",
#     default=0,
#     type=bool,
#     help="Build the bitcoin.blockqueue collection and populate it",
# )
@index.command()
@click.option(
    "--datadir",
    default=None,
    # required=True,
    type=str,
    help="The Bitcoin data directory wit the *.dat files",
)
@click.option(
    "--datafile",
    required=True,
    type=str,
    help="A Bitcoin file (*.dat)",
)
def direct(datadir, datafile):

    block = Block(datafile=datafile)
    block.next_block()
    # Initilize our bitcoin client
    # bitcoin = Bitcoin(rpcuser, rpcpassword, rpchost, rpcport)
    # info = bitcoin.getblockchaininfo()
    print("Hello")
