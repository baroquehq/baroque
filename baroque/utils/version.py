"""Utility functions for handling with Baroque version numbers"""

from baroque.constants import BAROQUE_VERSION


def version_to_string(version_tuple):
    """Turns a version tuple in the form (Major, Minor, Patch) into its
    dot-separated equivalent.

    Example:
        ``(3, 0, 1) --> "3.0.1"``

    Args:
        version_tuple (tuple): the version tuple

    Returns:
        str: The dot-separated version string

    """
    return '.'.join(map(str, version_tuple))


def get_baroque_version_string():
    """Gives the current Baroque version string.

    Returns:
        str: The current dot-separated Baroque version string

    """
    return version_to_string(BAROQUE_VERSION)
