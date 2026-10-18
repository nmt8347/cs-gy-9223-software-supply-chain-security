import base64
import json
from unittest.mock import patch

import main
from helpers import LOG_INDEX


def test_inclusion_success_verifies_signature_and_proof(capsys, tmp_path):
    artifact = tmp_path / "artifact.md"
    artifact.write_text("hello")

    body = {
        "spec": {
            "signature": {
                "content": base64.b64encode(b"sig").decode(),
                "publicKey": {"content": base64.b64encode(b"cert").decode()},
            }
        }
    }
    entry = {"body": base64.b64encode(json.dumps(body).encode()).decode()}
    proof = {
        "index": 5,
        "tree_size": 10,
        "leaf_hash": "leaf",
        "hashes": ["h1"],
        "root_hash": "root",
    }

    with patch("main.get_log_entry", return_value=entry), patch(
        "main.extract_public_key", return_value="pubkey"
    ) as mock_key, patch("main.verify_artifact_signature") as mock_sig, patch(
        "main.get_verification_proof", return_value=proof
    ), patch("main.verify_inclusion") as mock_incl:
        main.inclusion(LOG_INDEX, str(artifact))

    mock_key.assert_called_once_with(b"cert")
    mock_sig.assert_called_once_with(b"sig", "pubkey", str(artifact))
    mock_incl.assert_called_once_with(
        main.DefaultHasher, 5, 10, "leaf", ["h1"], "root"
    )
    assert "Successfully verified inclusion" in capsys.readouterr().out
