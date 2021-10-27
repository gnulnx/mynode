from datetime import datetime
from typing import NoReturn
import numpy as np
import hashlib
import json
from binascii import hexlify


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def format_hash(hash_):
    return str(hexlify(hash_[::-1]).decode("utf-8"))


def jprint(s):
    print(json.dumps(s, indent=4, sort_keys=True, default=str))


class Block:
    def __init__(self, datafile=None, datadir=None, *args, **kwargs):

        self.datafile = datafile
        self.datadir = datadir
        if self.datafile:
            self.f = open(self.datafile, "rb")

    def get_record(self):
        rectype = np.dtype(
            [
                ("magic_id", "<u4"),
                ("headerLength", "<u4"),
            ]
        )
        rec = np.fromfile(self.f, dtype=rectype, count=1)[0]
        header_length = rec["headerLength"]
        magic_id = rec["magic_id"]

        rectype = np.dtype(
            [
                ("versionNumber", "<u4"),
                ("prev_block", "<V", 32),
                ("merkleRoot", "<V", 32),
                ("ts", "<u4"),
                ("bits", "<u4"),
                ("nounce", "<u4"),
                ("txns", f"<V{header_length-80}"),  # This needs to be somethig else
            ]
        )
        rec = np.fromfile(self.f, dtype=rectype, count=1)[0]

        hash = format_hash(
            double_sha256(
                (
                    rec["versionNumber"].tobytes()
                    + rec["prev_block"].tobytes()
                    + rec["merkleRoot"].tobytes()
                    + rec["ts"].tobytes()
                    + rec["bits"].tobytes()
                    + rec["nounce"].tobytes()
                )
            )
        )
        return {
            "magic_id": magic_id,
            "header_length": header_length,
            "versionNumber": rec["versionNumber"],
            "prev_block": hash,
            "merkleRoot": rec["merkleRoot"],
            "ts": rec["ts"],
            "bits": rec["bits"],
            "nounce": rec["nounce"],
            "txns": rec["txns"],
        }

    def variable_int(self, bs, offset=0):
        first_byte = np.dtype([("val", "<u1")])

        rec = np.frombuffer(bs, dtype=first_byte, count=1, offset=0)[0]
        if rec["val"] < 253:
            return (rec["val"], 1)
        elif rec["val"] == 253:
            next_two_bytes = np.dtype([("val", "<u2")])
            rec = np.frombuffer(bs, dtype=next_two_bytes, count=1, offset=0)[0]
            return (rec["val"], 3)
        elif rec["val"] == 254:
            next_two_bytes = np.dtype([("val", "<u4")])
            rec = np.frombuffer(bs, dtype=next_two_bytes, count=1, offset=0)[0]
            return (rec["val"], 5)
        elif rec["val"] == 255:
            next_two_bytes = np.dtype([("val", "<u8")])
            rec = np.frombuffer(bs, dtype=next_two_bytes, count=1, offset=0)[0]
            return (rec["val"], 9)
        else:
            raise ValueError("Not a possible variable int")

    def next_block(self):
        block = self.get_record()
        txn_data = block["txns"]
        print(datetime.fromtimestamp(block["ts"]))
        print("nounce: %s" % block["nounce"])
        # Need to resolve transaction stuff
        print("len(txn_data): %s" % len(txn_data.item()))
        txn_count, offset = self.variable_int(txn_data)

        # Load the transactions
        block.update({"txns": []})
        for _ in range(txn_count.item()):
            txn, offset = self.read_transaction(txn_data, offset)
            # print(txn)
            # block["txns"].append(txn)
            # input()

        # print("After inputs")
        # input()

        print("txn_count: %s" % txn_count)
        print("Next offset: %s" % offset)
        len_txn_data = len(txn_data.item())
        blockSize = len_txn_data + 80  # 80 is the size of the header used
        block.update({"blockSize": blockSize})

        # del block["merkleRoot"]
        print(block)
        print("block")
        # input()
        jprint(block)
        # print(json.dumps(block, default=str))
        input()
        # print(txn_count, bytes_used)
        return block

    def read_transaction(self, bs, offset):
        recType = np.dtype([("txn_versionNumber", "<u4")])
        res = np.frombuffer(bs, dtype=recType, count=1, offset=0)[0]
        txn_versionNumber = res["txn_versionNumber"]

        offset += 4
        num_inputs, new_offset = self.variable_int(bs, offset)
        offset += new_offset

        results = {"inputs": [], "outputs": []}

        for _ in range(num_inputs):
            result, offset = self.read_input(bs, offset)
            results["inputs"].append(results)

        num_outputs, new_offset = self.variable_int(bs, offset)
        offset += new_offset

        for _ in range(num_outputs):
            result, offset = self.read_output(bs, offset)
            results["outputs"].append(result)

        return results, offset

    def read_output(self, bs, offset):
        # read value in satoshis
        recType = np.dtype([("value", "<u8")])
        resp = np.frombuffer(bs, dtype=recType, count=1, offset=offset)[0]
        offset += 8
        value = resp["value"]

        output_script_length, new_offset = self.variable_int(bs, offset)
        offset += new_offset

        recType = np.dtype([("script", "<V", output_script_length)])
        resp = np.frombuffer(bs, dtype=recType, count=1, offset=offset)[0]
        offset += output_script_length
        script = resp["script"]

        return {
            "value": value,
            "output_script_length": output_script_length,
            "script": script,
        }, offset

    def read_input(self, bs, offset):
        recType = np.dtype(
            [
                ("txn_hash", "<V", 32),
                ("txn_idx", "<u4"),
            ]
        )
        resp = np.frombuffer(bs, dtype=recType, count=1, offset=offset)[0]
        offset += 4
        offset += 32
        txn_hash = resp["txn_hash"]
        txn_idx = resp["txn_idx"]

        script_length, new_offset = self.variable_int(bs, offset)
        offset += new_offset
        recType = np.dtype(
            [
                ("script", "<V", script_length),
                ("seqNum", "<V", 4),
            ]
        )
        resp = np.frombuffer(bs, dtype=recType, count=1, offset=offset)[0]
        offset += 4
        offset += script_length
        script = resp["script"]
        seqNum = resp["seqNum"]

        hash = format_hash(
            double_sha256(
                (
                    txn_hash.tobytes()
                    + txn_idx.tobytes()
                    + script_length.tobytes()
                    + script.tobytes()
                    # + rec["bits"].tobytes()
                    # + rec["nounce"].tobytes()
                )
            )
        )

        return {
            "txn_hash": hash,
            "txn_idx": txn_idx,
            "script_length": script_length,
            "script": script,
            "seqNum": seqNum,
        }, offset
