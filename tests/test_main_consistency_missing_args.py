from unittest.mock import patch

import pytest

from helpers import PREV_ROOT, PREV_SIZE, TREE_ID, run_main

FULL_ARGS = {
    "--tree-id": TREE_ID,
    "--tree-size": str(PREV_SIZE),
    "--root-hash": PREV_ROOT,
}


@pytest.mark.parametrize(
    "missing, expected_message",
    [
        ("--tree-id", "please specify tree id"),
        ("--tree-size", "please specify tree size"),
        ("--root-hash", "please specify root hash"),
    ],
)
def test_main_consistency_requires_all_checkpoint_arguments(
    missing, expected_message, monkeypatch, capsys
):
    argv = ["--consistency"]
    for flag, value in FULL_ARGS.items():
        if flag != missing:
            argv += [flag, value]

    with patch("main.consistency") as mock_cons:
        run_main(monkeypatch, *argv)

    mock_cons.assert_not_called()
    assert expected_message in capsys.readouterr().out
