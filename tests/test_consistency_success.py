from unittest.mock import patch

import main
from helpers import PREV_ROOT, PREV_SIZE, TREE_ID, make_response


def test_consistency_success_fetches_proof_when_sizes_differ(capsys):
    prev = {"treeID": TREE_ID, "treeSize": PREV_SIZE, "rootHash": PREV_ROOT}
    latest_size = PREV_SIZE + 93
    latest = {"treeID": TREE_ID, "treeSize": latest_size, "rootHash": "latestroot"}

    with patch("main.get_latest_checkpoint", return_value=latest), patch(
        "main.requests.get", return_value=make_response(200, {"hashes": ["a", "b"]})
    ) as mock_get, patch("main.verify_consistency") as mock_verify:
        main.consistency(prev)

    mock_get.assert_called_once()
    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {
        "firstSize": PREV_SIZE,
        "lastSize": latest_size,
        "treeID": TREE_ID,
    }
    mock_verify.assert_called_once_with(
        main.DefaultHasher, PREV_SIZE, latest_size, ["a", "b"], PREV_ROOT, "latestroot"
    )
    assert "Consistency verification successful." in capsys.readouterr().out


def test_consistency_success_skips_proof_when_sizes_equal():
    prev = {"treeID": TREE_ID, "treeSize": PREV_SIZE, "rootHash": PREV_ROOT}
    same = {"treeID": TREE_ID, "treeSize": PREV_SIZE, "rootHash": PREV_ROOT}

    with patch("main.get_latest_checkpoint", return_value=same), patch(
        "main.requests.get"
    ) as mock_get, patch("main.verify_consistency") as mock_verify:
        main.consistency(prev)

    mock_get.assert_not_called()
    mock_verify.assert_called_once_with(
        main.DefaultHasher, PREV_SIZE, PREV_SIZE, [], PREV_ROOT, PREV_ROOT
    )
