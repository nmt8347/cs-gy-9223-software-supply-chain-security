from unittest.mock import patch

import main


def test_get_verification_proof_builds_expected_dict():
    entry = {
        "body": "BODY",
        "verification": {
            "inclusionProof": {
                "logIndex": 7,
                "treeSize": 20,
                "hashes": ["h1", "h2"],
                "rootHash": "root",
            }
        },
    }
    with patch("main.get_log_entry", return_value=entry), patch(
        "main.compute_leaf_hash", return_value="leafhash"
    ) as mock_leaf:
        proof = main.get_verification_proof(7)

    mock_leaf.assert_called_once_with("BODY")
    assert proof == {
        "index": 7,
        "tree_size": 20,
        "hashes": ["h1", "h2"],
        "root_hash": "root",
        "leaf_hash": "leafhash",
    }

    with patch("main.get_log_entry", return_value=None):
        assert main.get_verification_proof(7) is None
