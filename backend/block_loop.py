from server import bitcoin
from wallet.core.utils.jprint import jprint


info = bitcoin.getblockchaininfo()
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

for idx in range(height):
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
            ]:
                for address in scriptpubkey["addresses"]:
                    if address not in addresses:
                        addresses[address] = {"vins": [], "vouts": []}

                    addresses[address]["vouts"].append(tx)

                    if tx not in transactions:
                        transactions[tx] = {"vins": [], "vouts": []}

                    transactions[tx]["vouts"].append(address)

                    newAdd = True
            else:
                if "addresses" in scriptpubkey:
                    jprint(txn)
                    print("Whats up")
                    input()
                # else:
                #     print("Notimplemented: %s" % scriptpubkey["type"])

        if newAdd:
            # print(out)
            jprint(addresses)
            jprint(transactions)
            # input()
        # if "addresses" in out["scriptPubKey"]:
        #     jprint(out["scriptPubKey"])
        #     input()

        # print("end")
        # input()
