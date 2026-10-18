from unittest.mock import patch

import pytest

from helpers import run_main


@pytest.mark.parametrize("flag", ["-d", "--debug"])
def test_main_debug_flag_prints_banner(flag, monkeypatch, capsys):
    with patch("main.get_latest_checkpoint") as mock_cp, patch(
        "main.inclusion"
    ) as mock_incl, patch("main.consistency") as mock_cons:
        run_main(monkeypatch, flag)

    assert "enabled debug mode" in capsys.readouterr().out
    mock_cp.assert_not_called()
    mock_incl.assert_not_called()
    mock_cons.assert_not_called()
