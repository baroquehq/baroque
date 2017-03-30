from baroque.utils.version import version_to_string


def test_version_to_string():
    version_tuple = (5, 2, 9)
    expected = '5.2.9'
    assert version_to_string(version_tuple) == expected
