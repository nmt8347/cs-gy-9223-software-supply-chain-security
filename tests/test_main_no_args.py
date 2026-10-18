from unittest.mock import patch

from helpers import run_main


def test_main_without_arguments_does_nothing(monkeypatch, capsys):
    with patch("main.get_latest_checkpoint") as mock_cp, patch(
        "main.inclusion"
    ) as mock_incl, patch("main.consistency") as mock_cons:
        run_main(monkeypatch)

    mock_cp.assert_not_called()
    mock_incl.assert_not_called()
    mock_cons.assert_not_called()
    assert capsys.readouterr().out == ""
