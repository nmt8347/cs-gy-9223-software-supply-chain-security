from unittest.mock import patch

import main
from helpers import TREE_ID, make_response


def test_get_latest_checkpoint_success_and_failure():
    payload = {"treeID": TREE_ID, "treeSize": 100, "rootHash": "abc"}
    with patch("main.requests.get", return_value=make_response(200, payload)):
        assert main.get_latest_checkpoint() == payload

    with patch("main.requests.get", return_value=make_response(500)):
        assert main.get_latest_checkpoint() is None
