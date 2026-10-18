import pytest

import main
from helpers import LOG_INDEX


@pytest.mark.parametrize("value", [0, 1, "42", LOG_INDEX])
def test_validate_log_index_accepts_non_negative_integers(value):
    assert main.validate_log_index(value) is True
