import util
from crypto_helpers import make_ec_key, public_pem, sign


def test_verify_artifact_signature_tampered_artifact_reports_invalid(tmp_path, capsys):
    key = make_ec_key()
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"original content")
    signature = sign(key, b"original content")

    artifact.write_bytes(b"tampered content")
    util.verify_artifact_signature(signature, public_pem(key), str(artifact))

    assert "Signature is invalid" in capsys.readouterr().out
