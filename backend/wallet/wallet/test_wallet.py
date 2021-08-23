import pytest
from core import jprint, info  # noqa
from core.utils.encoding import base_10_to_16

from .wallet import Wallet


wallet_test_data = [
    (
        # Private Key
        "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
        {
            "passphrase": None,
            "private_key": "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
            "public_key:": "0250863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B2352",
            "address": "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs",
            "uncomp_public_key": "0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6",  # noqa
            "uncomp_address": "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM",
        },
    ),
    (
        "B18427B169E86DE681A1A62588E1D02AE4A7E83C1B413849989A76282A7B562F",
        {
            "passphrase": None,
            "private_key": "B18427B169E86DE681A1A62588E1D02AE4A7E83C1B413849989A76282A7B562F",
            "public_key:": "029C95E0949E397FACCECF0FE8EAD247E6FD082717E4A4A876049FB34A9ADED110",
            "address": "1AK5HTxzz7C57dDgfw8UctsNtg1sAwJ4XP",
            "uncomp_public_key": "049C95E0949E397FACCECF0FE8EAD247E6FD082717E4A4A876049FB34A9ADED110DFEA2EF691CC4A1410498F4C312F3A94318CD5B6F0E8E92051064876751C8404",  # noqa
            "uncomp_address": "12gFLYWpfnDTQ3JB5w5VDPpF5JQZnA1g1c",
        },
    ),
]


@pytest.mark.parametrize("private_key, expected", wallet_test_data)
def test_wallet_from_private_key(private_key, expected):
    w = Wallet.restore(private_key=private_key, test=True)
    details = w.details()
    # Wif not included in test data so remove it.
    del details["wif"]
    del details["wifc"]
    assert details == expected


wallet_one_plus_two_data = [
    (
        "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
        "B18427B169E86DE681A1A62588E1D02AE4A7E83C1B413849989A76282A7B562F",
        {
            "passphrase": None,
            "private_key": "CA65722CD418ED28EC369E36CFE3B7F3CC1CD035BFBF6469CE759FCA30AD6D54",
            "public_key:": "0336970CE32E14DC06AC50217CDCF53E628B32810707080D6848D9C8D4BE9FE461",
            "address": "1PaBgxrA2MzdBvHSCUFh66PndKf3eXiBad",
            "uncomp_public_key": "0436970CE32E14DC06AC50217CDCF53E628B32810707080D6848D9C8D4BE9FE461E100E705CCA9854436A1283210CCEFBB6B16CB9A86B009488922A8F302A27487",  # noqa
            "uncomp_address": "166ev9JXn2rFqiPSQAwM7qJYpNL1JrNf3h",
            "wif": "5KMRXGWiRFbM2c8NiNA3AzihkoCE6JieQpFJ3Wes8p9knMEzx3Z",
            "wifc": "L419EbU9p3QbQ63YqaNtb7m4tJtYnRCp87Y6E5t8HV7eEwXcoVte",
        },
    ),
    (
        "F4DF074F7871417EE9DEB3BCBF03DF59FE0CB1077AC76A76481A2E3853F5CBB8",
        "0377CA5AE8F5353FE2C161753AB4B166A357C663E9D79839C62D335BFA744BB2",
        {
            "passphrase": None,
            "private_key": "F856D1AA616676BECCA01531F9B890C0A164776B649F02B00E4761944E6A176A",
            "public_key:": "03D4FD4B9E6A73C00385FFA23C64511E3CE3173FD3A398BA8AA207042546F0BD97",
            "address": "1N7JCVMWcG1D14GMGhtupWMaGfWXuLiH8F",
            "uncomp_public_key": "04D4FD4B9E6A73C00385FFA23C64511E3CE3173FD3A398BA8AA207042546F0BD971135408E4D0241D45703CB456BAD56E2D60658FD54B3D97E5F6F0F94F9D85E7D",  # noqa
            "uncomp_address": "15NbXM3S9mKt1SVideuhaxGnBNUdPm5san",
            "wif": "5Khf56cbVEQP3KAZ1KJve4CDP9UqtyWWCQorhmApgS6oTAgRZ8C",
            "wifc": "L5YT35n7DcACHDBAGPp7kZ6VekRtpQRDsN5pNuxMT3nc2UT2LFfY",
        },
    ),
    (
        "AE655E267512EE60CE1399832684AA926D9A1539108D93581A928DBDA51F44C0",
        "34BF09F750BE770FFE4CC2718D5D8122F1FAFFA283F72B03C157AFB3B9F81CA8",
        {
            "passphrase": None,
            "private_key": "E324681DC5D16570CC605BF4B3E22BB55F9514DB9484BE5BDBEA3D715F176168",
            "public_key:": "03D61939DE8C7AD270972FC569A2E989A3F645B48632DFB7498A82C53ACE82EA35",
            "address": "15zokr86tRGiBydLKmJc3t9auSBtiHQw1n",
            "uncomp_public_key": "04D61939DE8C7AD270972FC569A2E989A3F645B48632DFB7498A82C53ACE82EA35B370430E4FFC3138B6402845F8BBBAB43733CCC54BEF03CD9412560B97B600AF",  # noqa
            "uncomp_address": "1HNapVoYwQGofujH1ejGPFjTqqqqkNi9Z",
            "wif": "5KYKdB5G9uPhsB27t2N7peAiwCJn68MnVVsGoHC6H1M61vydECi",
            "wifc": "L4qFCfTotJFDNTDwND2D7H3v6CuU1dUjnnQtjGTxHeXf8xzp4SYo",
        },
    ),
]


@pytest.mark.parametrize("priv_key1, priv_key2, expected", wallet_one_plus_two_data)
def test_wallet_restore_from_one_plus_two_private_key(priv_key1, priv_key2, expected):
    priv_key = base_10_to_16(int(priv_key1, 16) + int(priv_key2, 16))
    w = Wallet.restore(private_key=priv_key.upper(), test=True)
    assert w.details() == expected


wallet_one_times_two_data = [
    (
        "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
        "B18427B169E86DE681A1A62588E1D02AE4A7E83C1B413849989A76282A7B562F",
        {
            "passphrase": None,
            "private_key": "936B522B34313FC011FAB0E776EB52D47ADFA98F02BF2B70A248B849F3CD1465",
            "public_key:": "023A315ECE573AD101229795CECB7FC7E81E8C88A01125C86C320F9B86755BFD73",
            "address": "1Mu41SWr9RfywBADENveVE8fbpyWkrxtU4",
            "uncomp_public_key": "043A315ECE573AD101229795CECB7FC7E81E8C88A01125C86C320F9B86755BFD73C5B03D04130C50A10E80E3CE3F22FA670AA62C238CACC0648DD7AB93936DF900",  # noqa
            "uncomp_address": "12W5zRiwpYmDgA2QiJ9Zqu75CaCthEh793",
            "wif": "5JwDCzvnptzsR13LLHjTzwYWoUoyv92ZHukwLH18NJELXaBbqTc",
            "wifc": "L2AGsxgRGQWRWwBJL8rSAjk6Y9kNDYRsXdrvp5dZX13sBstJXnBq",
        },
    ),
    (
        "AE655E267512EE60CE1399832684AA926D9A1539108D93581A928DBDA51F44C0",
        "34BF09F750BE770FFE4CC2718D5D8122F1FAFFA283F72B03C157AFB3B9F81CA8",
        {
            "passphrase": None,
            "private_key": "C6F59F5EC332933B648A2AD0875DFAF53DD814B8B891CDF0BA3F6887B7C947FE",
            "public_key:": "020C2CCA3393924AB8921A1CDE3A78836DBC4864B47948002790E914F2526EBE2D",
            "address": "1JfrVqXXHbq5ZeJpa5MN2HZcDGkqfMvmW",
            "uncomp_public_key": "040C2CCA3393924AB8921A1CDE3A78836DBC4864B47948002790E914F2526EBE2DD411F34A610944BE72F411466E5593D77E578038DC0063434551411EA408A3BA",  # noqa
            "uncomp_address": "1NbnCxK83nDqJQxuFn9w3AJwh5hvTW4YdX",
            "wif": "5KKujXJEhShgkqPNZkNJJHuGuaCfgA1ZxkrjHfnySo5DgTmXqD7",
            "wifc": "L3tTkgj5TWSaUUZkBYR1MKbjD3YVhpmWV6aVeaDv8rMcy4HC6g8T",
        },
    ),
]


# @pytest.mark.parametrize("priv_key1, priv_key2, expected", wallet_one_times_two_data)
# def test_wallet_restore_from_one_times_two_private_key(priv_key1, priv_key2, expected):
#     priv_key = base_10_to_16((int(priv_key1, 16) * int(priv_key2, 16)))
#     print(int(priv_key1, 16))
#     print(int(priv_key2, 16))
#     print("multiple")
#     print(priv_key)
#     print("add")
#     print(base_10_to_16(int(priv_key1, 16) + int(priv_key2, 16)))
#     # input()
#     w = Wallet.restore(private_key=priv_key.upper(), test=True)
#     w.details(show=1)
#     info("output")
#     jprint(expected)
#     info("expected")
#     # input()
#     assert w.details() == expected


def test_wallet_restore_from_wif():
    w = Wallet.new(test=True)
    w2 = Wallet.restore(private_key=w.wif, test=True)
    assert w.details()["address"] == w2.details()["address"]


def test_wallet_restore_from_passphrase():
    w = Wallet.new(test=True)
    w2 = Wallet.restore(passphrase=w.details()["passphrase"], test=True)
    assert w.details()["address"] == w2.details()["address"]
