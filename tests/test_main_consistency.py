from unittest.mock import patch

from helpers import PREV_ROOT, PREV_SIZE, TREE_ID, run_main


def test_main_consistency_builds_prev_checkpoint_and_dispatches(monkeypatch):
    with patch("main.consistency") as mock_cons:
        run_main(
            monkeypatch,
            "--consistency",
            "--tree-id",
            TREE_ID,
            "--tree-size",
            str(PREV_SIZE),
            "--root-hash",
            PREV_ROOT,
        )

    mock_cons.assert_called_once_with(
        {"treeID": TREE_ID, "treeSize": PREV_SIZE, "rootHash": PREV_ROOT}, False
    )


def test_main_consistency_with_debug_passes_debug_true(monkeypatch):
    with patch("main.consistency") as mock_cons:
        run_main(
            monkeypatch,
            "-d",
            "--consistency",
            "--tree-id",
            TREE_ID,
            "--tree-size",
            str(PREV_SIZE),
            "--root-hash",
            PREV_ROOT,
        )

    _, debug = mock_cons.call_args[0]
    assert debug is True
