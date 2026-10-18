import util
from crypto_helpers import make_ec_key, public_pem, sign


def test_verify_artifact_signature_wrong_public_key_reports_invalid(tmp_path, capsys):
    signer = make_ec_key()
    other = make_ec_key()
    artifact = tmp_path / "artifact.md"
    data = b"hello rekor"
    artifact.write_bytes(data)

    util.verify_artifact_signature(sign(signer, data), public_pem(other), str(artifact))

    assert "Signature is invalid" in capsys.readouterr().out
