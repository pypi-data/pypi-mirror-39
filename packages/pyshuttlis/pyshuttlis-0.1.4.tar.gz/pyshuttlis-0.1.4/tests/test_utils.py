import pytest

from shuttlis.utils import one_or_none, one


@pytest.mark.parametrize('lizt,key,expected', [
    ([1, 2, 3], lambda x: x == 2, 2),
    (['a', 'b', 'c'], lambda x: x == 'c', 'c'),
    (['a', 'b', 'c'], lambda x: x == 'd', None),
])
def test_one_or_none(lizt, key, expected):
    actual = one_or_none(lizt, key)
    assert expected == actual


def test_one_or_none_raises_assertion_error_if_more_than_one_match():
    with pytest.raises(AssertionError) as e:
        one_or_none([1, 2, 2, 2], lambda x: x == 2)


@pytest.mark.parametrize('lizt,key,expected', [
    ([1, 2, 3], lambda x: x == 2, 2),
    (['a', 'b', 'c'], lambda x: x == 'c', 'c'),
])
def test_one(lizt, key, expected):
    actual = one(lizt, key)
    assert expected == actual


def test_one_raises_assertion_error_if_more_than_one_match():
    with pytest.raises(AssertionError) as e:
        one([1, 2, 2, 2], lambda x: x == 2)


def test_one_raises_assertion_error_if_none_match():
    with pytest.raises(AssertionError) as e:
        one([1, 2, 2, 2], lambda x: x == 4)
