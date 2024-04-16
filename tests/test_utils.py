import pytest
from datetime import datetime
from app import utils


@pytest.mark.parametrize('input_val, expected', [
    (1, 1),
    ('test', 'test'),
    (datetime(2023, 1, 1, 12), '2023-01-01T12:00:00')
])
def test_to_json_safe(input_val, expected):
    assert utils.to_json_safe(input_val) == expected
