import util
from crypto_helpers import make_ec_key, public_pem, sign


def test_verify_artifact_signature_valid_signature_prints_nothing(tmp_path, capsys):
    key = make_ec_key()
    artifact = tmp_path / "artifact.md"
    data = b"hello rekor"
    artifact.write_bytes(data)

    util.verify_artifact_signature(sign(key, data), public_pem(key), str(artifact))

    assert capsys.readouterr().out == ""
