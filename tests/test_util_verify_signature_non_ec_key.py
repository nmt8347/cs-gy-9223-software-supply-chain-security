import util
from crypto_helpers import make_rsa_public_pem


def test_verify_artifact_signature_non_ec_key_hits_generic_exception_handler(
    tmp_path, capsys
):
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"hello rekor")

    util.verify_artifact_signature(b"sig", make_rsa_public_pem(), str(artifact))

    out = capsys.readouterr().out
    assert "Exception in verifying artifact signature" in out
    assert "Signature is invalid" not in out
