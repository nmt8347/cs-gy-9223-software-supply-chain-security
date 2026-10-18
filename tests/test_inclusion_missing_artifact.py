from unittest.mock import patch

import main
from helpers import LOG_INDEX


def test_inclusion_reports_missing_artifact(capsys, tmp_path):
    missing = tmp_path / "does_not_exist.md"
    with patch("main.get_log_entry") as mock_entry:
        main.inclusion(LOG_INDEX, str(missing))

    mock_entry.assert_not_called()
    assert "does not exist" in capsys.readouterr().out
