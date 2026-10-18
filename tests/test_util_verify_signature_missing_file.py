import pytest

import util
from crypto_helpers import make_ec_key, public_pem


def test_verify_artifact_signature_missing_file_raises(tmp_path):
    key = make_ec_key()

    with pytest.raises(FileNotFoundError):
        util.verify_artifact_signature(
            b"sig", public_pem(key), str(tmp_path / "missing.md")
        )
