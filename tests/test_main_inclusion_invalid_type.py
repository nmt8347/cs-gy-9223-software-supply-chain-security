from unittest.mock import patch

import pytest

from helpers import run_main


def test_main_inclusion_rejects_non_integer_index(monkeypatch, capsys):
    with patch("main.inclusion") as mock_incl:
        with pytest.raises(SystemExit) as exc:
            run_main(monkeypatch, "--inclusion", "abc", "--artifact", "artifact.md")

    assert exc.value.code == 2
    assert "invalid int value" in capsys.readouterr().err
    mock_incl.assert_not_called()
