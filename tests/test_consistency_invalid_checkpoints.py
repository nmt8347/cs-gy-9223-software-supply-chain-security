from unittest.mock import patch

import pytest

import main
from helpers import PREV_ROOT, TREE_ID


@pytest.mark.parametrize(
    "prev, expected_message",
    [
        ({"treeID": TREE_ID, "treeSize": 10}, "missing key"),
        (
            {"treeID": TREE_ID, "treeSize": 0, "rootHash": PREV_ROOT},
            "invalid tree sizes",
        ),
        (
            {"treeID": TREE_ID, "treeSize": 5000, "rootHash": PREV_ROOT},
            "invalid tree sizes",
        ),
        (
            {"treeID": "999", "treeSize": 10, "rootHash": PREV_ROOT},
            "tree ID mismatch",
        ),
    ],
)
def test_consistency_rejects_invalid_checkpoints(prev, expected_message, capsys):
    latest = {"treeID": TREE_ID, "treeSize": 100, "rootHash": "latestroot"}
    with patch("main.get_latest_checkpoint", return_value=latest), patch(
        "main.requests.get"
    ) as mock_get, patch("main.verify_consistency") as mock_verify:
        main.consistency(prev)

    mock_get.assert_not_called()
    mock_verify.assert_not_called()
    assert expected_message in capsys.readouterr().out
