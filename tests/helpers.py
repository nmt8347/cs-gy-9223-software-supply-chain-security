from unittest.mock import MagicMock

TREE_ID = "1193050959916656506"
PREV_SIZE = 3179970807
PREV_ROOT = "7d11ecb2538fcb98aae1405d31a2df1416e89a5f96045ba2feb05057067eea8f"
LOG_INDEX = 3256683300


def make_response(status_code=200, payload=None):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = payload if payload is not None else {}
    return response

def run_main(monkeypatch, *argv):
    """Invoke main.main() with the given CLI arguments."""
    import main

    monkeypatch.setattr("sys.argv", ["main.py", *argv])
    main.main()
