from cryptography.hazmat.primitives import serialization

import util
from crypto_helpers import make_cert_pem, make_ec_key, public_pem


def test_extract_public_key_returns_pem_matching_certificate_key():
    key = make_ec_key()
    result = util.extract_public_key(make_cert_pem(key))

    assert result.startswith(b"-----BEGIN PUBLIC KEY-----")
    assert result == public_pem(key)
    # Result must be loadable as a public key.
    assert serialization.load_pem_public_key(result) is not None
