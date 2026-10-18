import json
from unittest.mock import patch

import pytest

from helpers import TREE_ID, run_main


@pytest.mark.parametrize("flag", ["-c", "--checkpoint"])
def test_main_checkpoint_prints_latest_checkpoint_as_json(flag, monkeypatch, capsys):
    checkpoint = {"treeID": TREE_ID, "treeSize": 100, "rootHash": "abc"}
    with patch("main.get_latest_checkpoint", return_value=checkpoint) as mock_cp:
        run_main(monkeypatch, flag)

    mock_cp.assert_called_once_with(False)
    assert json.loads(capsys.readouterr().out) == checkpoint
