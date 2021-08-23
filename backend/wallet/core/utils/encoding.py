import base58
import bech32
import binascii

BITCOIN_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_encode_hex_str(key):
    print(f"key: {key}")
    return base58.b58encode(bytes.fromhex(key), alphabet=BITCOIN_ALPHABET).decode(
        "utf-8"
    )


def bech32_encode_hex_str(key, testnet=False):
    # spk = binascii.unhexlify('0014751e76e8199196d454941c45d1b3a323f1433bd6')
    # spk = binascii.unhexlify(key)
    spk = bytes.fromhex(key)
    version = spk[0] - 0x50 if spk[0] else 0
    program = spk[2:]
    return bech32.encode("tb" if testnet else "bc", version, program)


def base58_wif_to_bytes(wif):
    data = base58.b58decode(wif)
    return data.hex().upper()


def base_10_to_16(chars, min_length=64):
    if isinstance(chars, str):
        chars = chars.encode()

    out = hex(chars)[2:]
    return out.zfill(min_length) if min_length else out
