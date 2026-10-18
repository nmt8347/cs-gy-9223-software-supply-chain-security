import base64
import hashlib

import pytest

from merkle_proof import compute_leaf_hash


def test_compute_leaf_hash_matches_rfc6962_leaf_hash():
    body = base64.b64encode(b"hello").decode()

    assert compute_leaf_hash(body) == hashlib.sha256(b"\x00hello").hexdigest()


def test_compute_leaf_hash_returns_lowercase_hex_of_sha256_length():
    result = compute_leaf_hash(base64.b64encode(b"").decode())

    assert len(result) == 64
    assert result == result.lower()
    assert result == hashlib.sha256(b"\x00").hexdigest()


def test_compute_leaf_hash_rejects_invalid_base64():
    with pytest.raises(Exception):
        compute_leaf_hash("not-valid-base64!!!")
