from unittest.mock import patch

import main
from helpers import LOG_INDEX, make_response


def test_get_log_entry_returns_entry_data():
    payload = {"uuid-1": {"body": "ZmFrZQ==", "logIndex": LOG_INDEX}}
    with patch("main.requests.get", return_value=make_response(200, payload)) as mock_get:
        result = main.get_log_entry(LOG_INDEX)

    assert result == payload["uuid-1"]
    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"logIndex": LOG_INDEX}
