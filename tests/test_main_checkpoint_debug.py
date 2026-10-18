from unittest.mock import patch

from helpers import TREE_ID, run_main


def test_main_checkpoint_with_debug_passes_debug_true(monkeypatch, capsys):
    checkpoint = {"treeID": TREE_ID, "treeSize": 100, "rootHash": "abc"}
    with patch("main.get_latest_checkpoint", return_value=checkpoint) as mock_cp:
        run_main(monkeypatch, "-c", "-d")

    mock_cp.assert_called_once_with(True)
    assert "enabled debug mode" in capsys.readouterr().out
