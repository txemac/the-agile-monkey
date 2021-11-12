from datetime import datetime
from uuid import UUID


def assert_dicts(original, expected):
    """
    Assert that check that the dict body contains all keys in expected.
    And the values are the same.
    If a value in expected contains "*" the value in body can be any value.
    If a value is a dict, check the dict inside.
    If a value is a list, check the list inside.

    :param Dict original: original dict
    :param Dict expected: expected dict
    """
    for key in expected.keys():
        assert key in original.keys(), key
        if type(original[key]) == dict:
            assert type(expected[key]) == dict
            assert_dicts(original=original[key], expected=expected[key])
        elif type(original[key]) == list:
            assert type(expected[key]) == list
            assert_lists(original=original[key], expected=expected[key])
        elif (type(original[key]) == datetime or type(expected[key]) == datetime) and expected[key] != "*":
            assert_datetime(original=original[key], expected=expected[key])
        elif (type(original[key]) == UUID or type(expected[key]) == UUID) and expected[key] != "*":
            assert str(original[key]) == str(expected[key]), f"key: {key}: {original[key]} - {expected[key]}"
        elif not expected[key] == "*":
            assert original[key] == expected[key], f"key: {key}: {original[key]} - {expected[key]}"


def assert_lists(original, expected, sort=None):
    """
    Assert that check to lists. Check the len of both list and the content.

    :param List original: original list
    :param List expected: expected list
    :param str sort: sort objects list by sort field.
    """
    assert len(original) == len(expected), len(original)

    if sort is not None:
        original = sorted(original, key=lambda x: x.__getattribute__(sort))
        expected = sorted(expected, key=lambda x: x.__getattribute__(sort))

    for i in range(len(original)):
        if type(original[i]) == dict:
            assert type(expected[i]) == dict, type(expected[i])
            assert_dicts(original=original[i], expected=expected[i])
        elif type(original[i]) == list:
            assert type(expected[i]) == list, type(expected[i])
            assert_lists(original=original[i], expected=expected[i])
        elif not expected[i] == "*":
            assert original[i] == expected[i], original[i]


def assert_datetime(original, expected):
    """
    Assert dates values.

    :param original: original
    :param expected: expected
    """
    if type(original) is not str:
        original = datetime.isoformat(original)

    if type(expected) is not str:
        expected = datetime.isoformat(expected)

    assert original[:19] == expected[:19]
