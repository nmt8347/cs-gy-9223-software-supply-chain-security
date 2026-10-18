import pytest

import main


@pytest.mark.parametrize("value", [-1, "-5", "abc", "1.5", ""])
def test_validate_log_index_rejects_invalid_values(value):
    assert main.validate_log_index(value) is False
