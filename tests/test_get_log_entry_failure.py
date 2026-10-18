from unittest.mock import patch

import main
from helpers import LOG_INDEX, make_response


def test_get_log_entry_returns_none_on_bad_index_or_http_error():
    with patch("main.requests.get") as mock_get:
        assert main.get_log_entry(-1) is None
        mock_get.assert_not_called()

    with patch("main.requests.get", return_value=make_response(404)):
        assert main.get_log_entry(LOG_INDEX) is None
