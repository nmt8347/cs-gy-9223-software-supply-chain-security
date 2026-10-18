import util
from crypto_helpers import make_ec_key, public_pem


def test_verify_artifact_signature_malformed_signature_reports_invalid(tmp_path, capsys):
    key = make_ec_key()
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"hello rekor")

    util.verify_artifact_signature(b"garbage", public_pem(key), str(artifact))

    assert "Signature is invalid" in capsys.readouterr().out
