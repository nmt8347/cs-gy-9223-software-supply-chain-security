from unittest.mock import patch

from helpers import LOG_INDEX, PREV_ROOT, PREV_SIZE, TREE_ID, run_main


def test_main_runs_all_requested_operations_in_order(monkeypatch):
    calls = []
    checkpoint = {"treeID": TREE_ID, "treeSize": 100, "rootHash": "abc"}

    with patch(
        "main.get_latest_checkpoint",
        side_effect=lambda debug: calls.append("checkpoint") or checkpoint,
    ), patch(
        "main.inclusion", side_effect=lambda *a: calls.append("inclusion")
    ), patch(
        "main.consistency", side_effect=lambda *a: calls.append("consistency")
    ):
        run_main(
            monkeypatch,
            "-c",
            "--inclusion",
            str(LOG_INDEX),
            "--artifact",
            "artifact.md",
            "--consistency",
            "--tree-id",
            TREE_ID,
            "--tree-size",
            str(PREV_SIZE),
            "--root-hash",
            PREV_ROOT,
        )

    assert calls == ["checkpoint", "inclusion", "consistency"]
