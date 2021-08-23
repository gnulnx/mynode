import pytest

from core.utils.wallet import (
    plain_hash,
    binary_hash,
    double_hash,
    create_private_key,
    wif_to_private_key,
    create_public_keys,
    private_key_to_address,
)
from core.utils.hash import sha256_ripemd_double_hash
from core.utils.encoding import base58_encode_hex_str, base58_wif_to_bytes


# A good site for test data
# http://gobittest.appspot.com/PrivateKey


plain_test_data = [
    (
        "803133293B7827ED422EA95FF7E6B92145FAA6A22DE1896043F457306AF4CF5B42",
        "F5A3CF1E170C27BEFA81A25E4ECA1B1E9BE1B822DFE4095B82059B29A094784D",
    )
]


@pytest.mark.parametrize("initial, expected", plain_test_data)
def test_plain_hash(initial, expected):
    output = plain_hash(initial)

    assert output == expected


binary_test_data = [
    (
        "807542FB6685F9FD8F37D56FAF62F0BB4563684A51539E4B26F0840DB361E0027C",
        "7DE4708EB23AB611371BB778FC0C8BDE80394AB2D8704D7129FB5771E2F1730D",
    ),
    (
        "C03BAFA8FE6D2EFB97169A6F8E8DF32219FC324C636D10DC89A503CFC3927613",
        "DADBA0D5DB52AA9E94BA40882812B262A03C1BAFE6AA911B5E839554B46F6E9F",
    ),
    (
        "C1E0C8A2389B17EB0212DD363A181E9F6564FF1355D59EED02E4EB179947E7A1",
        "5E5DE8C631429D1F6C1F5805B688A6CC9B3C22E54FE59931312BE76A56DCED06",
    ),
]


@pytest.mark.parametrize("initial, expected", binary_test_data)
def test_binary_hash(initial, expected):
    output = binary_hash(initial)

    assert output == expected


double_hash_data = [
    # https://bitcoin.stackexchange.com/questions/8247/how-can-i-convert-a-sha256-hash-into-a-bitcoin-base58-private-key
    (
        "807542FB6685F9FD8F37D56FAF62F0BB4563684A51539E4B26F0840DB361E0027C",
        "CD5C4A8E03DFBB0E3AA021C2D74A9EAA43CE4C9CB1B20FC88729A7A5834141CA",
        True,
    ),
    # https://medium.com/@hlopez_/how-are-public-and-private-keys-created-in-bitcoin-f90b2b88f40a
    (
        "803133293B7827ED422EA95FF7E6B92145FAA6A22DE1896043F457306AF4CF5B42",
        "58DAE61C47E89B61FFF699B413A8922AF5C6F1AB9FE45ABBBBE6281547FC0904",
        False,
    ),
    (
        "80BD813B9BFE1F85FD006227CFF5BD69D9BBEF68367C130E674AAA085381258D9E",
        "5E5DE8C631429D1F6C1F5805B688A6CC9B3C22E54FE59931312BE76A56DCED06",
        True,
    ),
    # This uses a different method
    # https://en.bitcoin.it/wiki/Wallet_import_format
    (
        "800C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D",
        "507A5B8DFED0FC6FE8801743720CEDEC06AA5C6FCA72B07C49964492FB98A714",
        True,
    ),
]


@pytest.mark.parametrize("initial, expected, binary", double_hash_data)
def test_double_hash(initial, expected, binary):
    assert double_hash(initial, binary=binary) == expected


private_key_data = [
    (
        "801DFA18F3C273D9AA6477E0183C6030E315176A174B8B5FFE7A33EAC469EFDCB7DADBA0D5",
        "5J3VJVAFwUJZp5NNxXDDcq17ruGvui1TCRABrPCvG8wgrF8YWE8",
    ),
    (
        "807542FB6685F9FD8F37D56FAF62F0BB4563684A51539E4B26F0840DB361E0027CCD5C4A8E",
        "5JhvsapkHeHjy2FiUQYwXh1d74evuMd3rGcKGnifCdFR5G8e6nH",
    ),
    (
        "803133293B7827ED422EA95FF7E6B92145FAA6A22DE1896043F457306AF4CF5B4258DAE61C",
        "5JBxKqYKzzoHrzeqwp6zXk8wZU3Ah94ChWAinSj1fYmyJvJS5rT",
    ),
]


@pytest.mark.parametrize("initial, expected", private_key_data)
def test_base58_encode_hex_str(initial, expected):
    assert base58_encode_hex_str(initial) == expected


create_private_key_data = [
    (
        "AofidowXhk&)):@:@9727929Hcks&&&(nkhgiowiwj919283$’@bnwkiHhVjKihUNnkllswiwi9@/93938’bbndkk!?,(ikjqlwlw188020$n€¥¥Hbnk",  # noqa
        "5JBxKqYKzzoHrzeqwp6zXk8wZU3Ah94ChWAinSj1fYmyJvJS5rT",
        False,
    ),
    (
        "AofidowXhk&)):@:@9727929Hcks&&&(nkhgiowiwj919283$’@bnwkiHhVjKihUNnkllswiwi9@/93938’bbndkk!?,(ikjqlwlw188020$n€¥¥Hbnk",  # noqa
        "5JBxKqYKzzoHrzeqwp6zXk8wZU3Ah94ChWAinSj1fYmyJy8Mxop",
        True,
    ),
]


@pytest.mark.parametrize("initial, expected, binary", create_private_key_data)
def test_create_private_key(initial, expected, binary):
    initial = initial.encode("utf-8")
    assert create_private_key(initial, binary=binary) == expected


def test_create_private_key_bytes_only():
    initial = "AofidowXhk&)):@:@9727929Hcks&&&(nkhgiowiwj919283$’@bnwkiHhVjKihUNnkllswiwi9@/93938’bbndkk!?,(ikjqlwlw188020$n€¥¥Hbnk"  # noqa
    with pytest.raises(ValueError):
        create_private_key(initial, binary=True)


wif_to_bytes = [
    (
        "5KFkEAC756myc65AFGXbiz9aLasgiHTHya58pLrkLpqMXdfA99F",
        "80BD813B9BFE1F85FD006227CFF5BD69D9BBEF68367C130E674AAA085381258D9E5E5DE8C6",
    )
]


@pytest.mark.parametrize("wif, expected", wif_to_bytes)
def test_base58_wif_to_bytes(wif, expected):
    assert base58_wif_to_bytes(wif) == expected


wif_to_private_key_data = [
    (
        "5KFkEAC756myc65AFGXbiz9aLasgiHTHya58pLrkLpqMXdfA99F",
        "BD813B9BFE1F85FD006227CFF5BD69D9BBEF68367C130E674AAA085381258D9E",
    )
]


@pytest.mark.parametrize("wif, expected", wif_to_private_key_data)
def test_wif_to_private_key(wif, expected):
    assert wif_to_private_key(wif) == expected


# This data came from
# https://gobittest.appspot.com/VanityAll
private_public_data = [
    (
        "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
        (
            "0250863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B2352",
            "0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6",  # noqa
        ),
    ),
    # (
    #     "B18427B169E86DE681A1A62588E1D02AE4A7E83C1B413849989A76282A7B562F",
    #     "049C95E0949E397FACCECF0FE8EAD247E6FD082717E4A4A876049FB34A9ADED110DFEA2EF691CC4A1410498F4C312F3A94318CD5B6F0E8E92051064876751C8404",  # noqa
    # ),
    # (
    #     "134385546D48F327ED3267E736467C1304F2127252207DEDED9D02E22EBAFAFC",
    #     "04766F5C9BE7F423BF7090E23272A8E2BEE4180D6B9D266A41E0EF7B0A27D8DE3703322F066DE4B9D8110CBB5CF5698A10BAC1C9A7DE1C490F4DF7CEEE68D4C6B3",  # noqa
    # ),
    # (
    #     "B4E54C207380D4B9E5FD111B6F48DF1DBC30E1DD9170153A80B0957E575924D2",
    #     "04A65491F0D908D41054EFD37658A334435393869AA1E13223504F3E520AF371302D902D9F523274C3659623A7438019C368C0968A100657F24173AF250EA13D4D",  # noqa
    # ),
    # (
    #     "F5494A0202ED75BE105D2525199E2F74A6E74EC47E5505F199FE28C8A973A68B",
    #     "04C60F9CA9789D30C6EEC3917333C1E76B8ABD53494A2F5E450A1D775A0167FDFD52AA8F8FE59D6C7A1E21AB78F46BA61DCD70909F808D8D3D0ED18CABAD791A49",
    # ),
    # (
    #     "43373431BF2338EA42BD64617785B9E12CC93BF1354F8AA4615E199D777967CE",
    #     "04C56E0E5F99F9C2C7F919ABEBE06A4BF774F82426B1090E965C1D0AC167EF33E85F97B34FC40607ECFECB2743AA2B8E5B92D74704D3EDD5D468E6E0E574B054F6",
    # ),
    # (
    #     "D2666323BBA1EA74641760C5A7DCBDE033745EBEB4CEBBCFBA00C7CE9ECAFB59",
    #     "04361935D4CFD9973D0D25D096F3DFDF4FFE57695D0C42771D4CB87AD2AE779A56E0B85B8E3E5907D32EA2159DDE32EB76BC6B242CD3E09B437FF5692B4E8E0FB2",
    # ),
    # (
    #     "18A2FCC8D87A5DD1FE6A4B851117BA4B8BAC72813A681DD71443A9F1F2E8285F",
    #     "04EFDEB1A0C8950D0646BD55613BA53AFBC90673D5A5E471C829B69CE5B79377CBB210635EEBDD357EC26B7626268A7949B0378D7245002CD49141B7EFDD524235",
    # ),
    # (
    #     "A79A48CB6E33CFBE65B8496944FA6E1235CDE37B09B3A3497889F59761CC48D8",
    #     "04238C3FC8889D8F546C779240B2CC6E4D689F95848E7020F6AF1C0F85E56C8A3405201A4A7DAD9EE586523441100756E94EA6FC0387321ACAEC627FD572966011",
    # ),
    # (
    #     "55283FD34E06ABBEC36B411B747C8EAEBE89A50F7559AA4181F34F40377B8607",
    #     "04C8C286C10BA698C758017D29981D55ED0F282C009E404BFB0C2C84D0C2E42FA4CDCE844249949053DBDE1DDDB4C07CCEABD5D4A88E7D8EDCBC9BC2F6336332D0",
    # ),
]


@pytest.mark.parametrize("priv_key, expected", private_public_data)
def test_create_public_keys(priv_key, expected):
    """
    Convert a priv_key to an uncompressed public key.
    Step 0 -> 1
    http://gobittest.appspot.com/Address
    """
    assert create_public_keys(priv_key) == expected


uncomprssed_address_data = [
    (
        "0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6",  # noqa
        "010966776006953D5567439E5E39F86A0D273BEE",
    ),
    (
        "04F8A24DCA93CEDB5E2F197214BD09AD49D82412F6AFE01B0044CDA1F1208CA7A6006B141EE5E465BD076B5402443F9B73C78D2384879FB84D0FCF599893C89ECE",  # noqa
        "E2C33C42752B85A5C91DB092A511D0A21D6DC9B0",
    ),
    (
        "04ED4300F769A07079A49C705B27B0B131128DC0B6C10F19E5E46BA2C4BBA25F6BFDDEA7224EBE0C2E12716C2492DF784B9A451CCDE5D190343CBCE2991F0939DC",  # noqa
        "D531B005794D9135FECE6557738E7C60B712230B",
    ),
]


@pytest.mark.parametrize("uncomp_pub_key, expected", uncomprssed_address_data)
def test_sha256_ripemd_double_hash(uncomp_pub_key, expected):
    """
    Double hash the uncompressed pub_key;  sha256 -> ripemd160
    Steps: 1 -> 3
    http://gobittest.appspot.com/Address
    """
    assert sha256_ripemd_double_hash(uncomp_pub_key, digest=False) == expected


private_key_to_addr_data = [
    (
        "18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725",
        (
            "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs",
            "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM",
        ),
    )
    # (
    #     "3277DD14D09BFBBF37913CD19A2F9803B54127BCCB511A7425174017F60FF4B2",
    #     "1LSGTDPuhQo6VGnBALdLP3QJHP4BSoz9Mv",
    # ),
    # (
    #     "E70407E4D2A3BAF16B76DA0D948BB1F0ECF42A5852590DE79CA3E37FDEA6CC30",
    #     "1DkCgaKqNyysPtfaHesKsmEBiHSJzFXj4M",
    # ),
    # (
    #     "1DAC9E978DE33C40DF0483E3A29AF6F030D9C233882489F1F6E6D8C3FAE2DA3D",
    #     "1MAHZh9dd3xNRwu73n5aydC6eYMTvZck88",
    # ),
    # (
    #     "FA709F89A3BCB10CCFFD6486ACB390F7465C2473951FEBD84CDDE07DE51A8F91",
    #     "1FFVcd1avXsWFQyAM6qLyPnxUjvjy8FY1h",
    # ),
    # (
    #     "5D826C84542AD4B0DD2147338ED93032830E21AC67AEDC254DDDA88A517606CB",
    #     "1CZsQMtfP1zR9AHX7gLzeK8H6Yr4McysF5",
    # ),
]


@pytest.mark.parametrize("priv_key, expected", private_key_to_addr_data)
def test_private_key_to_address(priv_key, expected):
    assert private_key_to_address(priv_key) == expected
