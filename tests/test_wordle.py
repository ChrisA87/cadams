import pytest
from app.wordle import wordle


@pytest.fixture
def dummy_corpus():
    yield ['cat', 'dog', 'bat', 'bad', 'eat', 'tan', 'ant', 'tea',
           'seat', 'leaf', 'beat', 'deaf', 'half']


def test_filter_numeric():
    result = wordle.filter_numeric(['cat', 'b4t', 'dog', 'd0ge'])
    assert result == ['cat', 'dog']


def test_return_candidates__include_exclude_is_None__3_letters(dummy_corpus):
    result = wordle.return_candidates('___', corpus=dummy_corpus)
    assert result == ['ant', 'bad', 'bat', 'cat', 'dog', 'eat', 'tan', 'tea']


def test_return_candidates__include_exclude_str__4_letters(dummy_corpus):
    result = wordle.return_candidates('___t', include_letters='ae', exclude_letters='fd', corpus=dummy_corpus)
    assert result == ['beat', 'seat']
