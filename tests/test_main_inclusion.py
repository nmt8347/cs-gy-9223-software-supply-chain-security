from unittest.mock import patch

from helpers import LOG_INDEX, run_main


def test_main_inclusion_dispatches_with_index_and_artifact(monkeypatch):
    with patch("main.inclusion") as mock_incl:
        run_main(
            monkeypatch, "--inclusion", str(LOG_INDEX), "--artifact", "artifact.md"
        )

    mock_incl.assert_called_once_with(LOG_INDEX, "artifact.md", False)


def test_main_inclusion_with_debug_passes_debug_true(monkeypatch):
    with patch("main.inclusion") as mock_incl:
        run_main(
            monkeypatch,
            "-d",
            "--inclusion",
            str(LOG_INDEX),
            "--artifact",
            "artifact.md",
        )

    mock_incl.assert_called_once_with(LOG_INDEX, "artifact.md", True)
