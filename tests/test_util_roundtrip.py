import util
from crypto_helpers import make_cert_pem, make_ec_key, sign


def test_extract_then_verify_roundtrip_with_certificate(tmp_path, capsys):
    key = make_ec_key()
    artifact = tmp_path / "artifact.md"
    data = b"signed with the cert's key"
    artifact.write_bytes(data)

    public_key = util.extract_public_key(make_cert_pem(key))
    util.verify_artifact_signature(sign(key, data), public_key, str(artifact))

    assert capsys.readouterr().out == ""
