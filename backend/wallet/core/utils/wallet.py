import hashlib  # noqa
import base58  # noqa
from mnemonic import Mnemonic
import warnings
from fastecdsa.curve import secp256k1 as fastecdsa_secp256k1
from fastecdsa import keys as fastecdsa_keys
from .hash import (
    binary_hash,
    plain_hash,
    double_hash,
    sha256_ripemd_double_hash,
)
from .encoding import (
    base58_encode_hex_str,
    base58_wif_to_bytes,
    base_10_to_16,
    bech32_encode_hex_str,
)


def wif_to_private_key(wif, compressed=False):
    if compressed:
        return base58_wif_to_bytes(wif)[:-10][2:]
    else:
        return base58_wif_to_bytes(wif)[:-8][2:]


# TODO This still needs unit tests
def compute_wif(key, prefix="80", compressed=False, binary=True):
    """
    Prefix will change based on testnet and mainnet
    """
    # Create the initial key with 80 in front.  Bitcoin private keys all start with 5.
    # prefix = "EF"
    key = prefix + key
    if compressed:
        key = f"{key}01"

    # double hash.
    checksum = double_hash(key, binary=binary)[:8]

    key = f"{key}{checksum}"

    # return base58 encoded key as string
    return base58_encode_hex_str(key)


def create_passphrase(language="english", strength=128):
    mnemo = Mnemonic(language)
    words = mnemo.generate(strength=strength)
    words.encode("utf-8")
    return words


def private_key_from_passphrase(passphrase, initial_hashes=100000):
    private_key = passphrase
    try:
        private_key = plain_hash(private_key)
        for a in range(initial_hashes - 1):
            private_key = binary_hash(private_key)

        if int(private_key, 16) < 2 ** 256:
            return private_key
        else:
            return None
    except Exception:
        warnings.warn("Passphrase(%s) could not be hashed" % passphrase)
        return None


def create_private_key(
    _str=None, binary=True, strength=128, language="english", initial_hashes=1
):
    """
    Approach taken from
    https://medium.com/@hlopez_/how-are-public-and-private-keys-created-in-bitcoin-f90b2b88f40a
    and
    https://bitcoin.stackexchange.com/questions/8247/how-can-i-convert-a-sha256-hash-into-a-bitcoin-base58-private-key
    """
    if not _str:
        _str = create_passphrase(language=language, strength=strength)

    if not isinstance(_str, bytes):
        raise ValueError("String not allowed.  Must be bytes")

    key = private_key_from_passphrase(_str, initial_hashes=initial_hashes)
    return compute_wif(key, binary=binary)


def create_public_keys(private_key):
    """"""
    if isinstance(private_key, str):
        private_key = int(private_key, 16)

    points = fastecdsa_keys.get_public_key(private_key, fastecdsa_secp256k1)
    x = base_10_to_16(points.x)
    y = base_10_to_16(points.y)

    uncomp_public_key = "04%s%s" % (x, y)
    if int(y, 16) % 2:
        public_key = "03%s" % x
    else:
        public_key = "02%s" % x

    return public_key.upper(), uncomp_public_key.upper()


def private_key_to_public_key(priv_key, testnet=False):
    pub_key, uncomp_pub_key = create_public_keys(priv_key)
    uncomp_pub_key_hash = sha256_ripemd_double_hash(uncomp_pub_key, digest=False)
    pub_key_hash = sha256_ripemd_double_hash(pub_key, digest=False)

    # Add the network byte
    # network_byte = "
    network_byte = "6F" if testnet else "00"
    print("network_byte: %s" % network_byte)
    uncomp_pub_key_hash_with_network_byte = f"{network_byte}{uncomp_pub_key_hash}"
    dsha256 = double_hash(uncomp_pub_key_hash_with_network_byte, binary=True)
    uncompressed_bitcoin_public_key = (
        f"{uncomp_pub_key_hash_with_network_byte}{dsha256[:8]}"
    )

    pub_key_hash_with_network_byte = f"{network_byte}{pub_key_hash}"
    dsha256 = double_hash(pub_key_hash_with_network_byte, binary=True)
    bitcoin_public_key = f"{pub_key_hash_with_network_byte}{dsha256[:8]}"

    return bitcoin_public_key, uncompressed_bitcoin_public_key


def private_key_to_address(priv_key, testnet=False):
    """
    Based on tests here:
    http://gobittest.appspot.com/Address
    """
    bitcoin_public_key, uncompressed_bitcoin_public_key = private_key_to_public_key(
        priv_key, testnet=testnet
    )
    print(bech32_encode_hex_str(bitcoin_public_key))
    print(bech32_encode_hex_str(uncompressed_bitcoin_public_key))
    return (
        base58_encode_hex_str(bitcoin_public_key),
        base58_encode_hex_str(uncompressed_bitcoin_public_key),
    )
