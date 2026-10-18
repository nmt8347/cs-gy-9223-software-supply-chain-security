import hashlib

from merkle_proof import DefaultHasher, Hasher


def test_hasher_applies_rfc6962_domain_separation():
    left, right = b"L" * 32, b"R" * 32

    assert DefaultHasher.hash_leaf(b"data") == hashlib.sha256(b"\x00data").digest()
    assert (
        DefaultHasher.hash_children(left, right)
        == hashlib.sha256(b"\x01" + left + right).digest()
    )
    assert DefaultHasher.empty_root() == hashlib.sha256(b"").digest()
    assert DefaultHasher.size() == 32


def test_hasher_leaf_and_node_hashes_are_domain_separated():
    data = b"A" * 32 + b"B" * 32
    assert DefaultHasher.hash_leaf(data) != DefaultHasher.hash_children(
        b"A" * 32, b"B" * 32
    )


def test_hasher_supports_custom_hash_function():
    hasher = Hasher(hashlib.sha512)

    assert hasher.size() == 64
    assert hasher.hash_leaf(b"x") == hashlib.sha512(b"\x00x").digest()
