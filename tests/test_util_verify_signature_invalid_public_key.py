import pytest

import util


@pytest.mark.parametrize("bad_key", [b"", b"not a pem key"])
def test_verify_artifact_signature_invalid_public_key_raises(bad_key, tmp_path):
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"hello rekor")

    with pytest.raises(ValueError):
        util.verify_artifact_signature(b"sig", bad_key, str(artifact))
