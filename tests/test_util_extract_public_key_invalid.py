import pytest

import util


@pytest.mark.parametrize("bad_cert", [b"", b"not a certificate", b"-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----\n"])
def test_extract_public_key_rejects_invalid_certificate(bad_cert):
    with pytest.raises(ValueError):
        util.extract_public_key(bad_cert)
