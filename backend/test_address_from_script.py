from backend.models.transaction import Transaction, utils
from backend.wallet.core.utils.encoding import *
from backend.wallet.core.utils.jprint import jprint


def test_address_from_pubkey():
    scriptpubkey = {
        "scriptPubKey": {
            "asm": "04c9560dc538db21476083a5c65a34c7cc219960b1e6f27a87571cd91edfd00dac16dca4b4a7c4ab536f85bc263b3035b762c5576dc6772492b8fb54af23abff6d OP_CHECKSIG",
            "hex": "4104c9560dc538db21476083a5c65a34c7cc219960b1e6f27a87571cd91edfd00dac16dca4b4a7c4ab536f85bc263b3035b762c5576dc6772492b8fb54af23abff6dac",
            "type": "pubkey",
        },
    }

    address = utils.address_from_pubkey(scriptpubkey["scriptPubKey"])
    assert address == "1Miuw7ifaTYY5qrzKYFcTDiojSFxRfAqwP"

    scriptpubkey = {
        "scriptPubKey": {
            "asm": "043987a76015929873f06823f4e8d93abaaf7bcf55c6a564bed5b7f6e728e6c4cb4e2c420fe14d976f7e641d8b791c652dfeee9da584305ae544eafa4f7be6f777 OP_CHECKSIG",
            "hex": "41043987a76015929873f06823f4e8d93abaaf7bcf55c6a564bed5b7f6e728e6c4cb4e2c420fe14d976f7e641d8b791c652dfeee9da584305ae544eafa4f7be6f777ac",
            "type": "pubkey",
        },
    }
    address = utils.address_from_pubkey(scriptpubkey["scriptPubKey"])
    assert address == "18KrJNtPVu6LWRNPQReqF29iFm7vDhirMk"


def test_address_from_pubkeyhash():
    scriptpubkey = {
        "scriptPubKey": {
            "addresses": ["12higDjoCCNXSA95xZMWUdPvXNmkAduhWv"],
            "asm": "OP_DUP OP_HASH160 12ab8dc588ca9d5787dde7eb29569da63c3a238c OP_EQUALVERIFY OP_CHECKSIG",
            "hex": "76a91412ab8dc588ca9d5787dde7eb29569da63c3a238c88ac",
            "reqSigs": 1,
            "type": "pubkeyhash",
        },
    }
    address = utils.address_from_pubkeyhash(scriptpubkey["scriptPubKey"])
    assert address == "12higDjoCCNXSA95xZMWUdPvXNmkAduhWv"
    pass


def test_txn_get_address():
    txid = "6f7cf9580f1c2dfb3c4d5d043cdbb128c640e3f20161245aa7372e9666168516"
    tx = Transaction(txid)
    assert len(tx.outputs) == 1
    assert tx.outputs[0]["address"] == "12higDjoCCNXSA95xZMWUdPvXNmkAduhWv"
    assert tx.outputs[0]["value"] == 100

    assert len(tx.inputs) == 2
    assert tx.inputs[0]["address"] == "1Miuw7ifaTYY5qrzKYFcTDiojSFxRfAqwP"
    assert tx.inputs[0]["value"] == 50

    assert tx.inputs[1]["address"] == "18KrJNtPVu6LWRNPQReqF29iFm7vDhirMk"
    assert tx.inputs[1]["value"] == 50

    assert tx.coinbase == False
