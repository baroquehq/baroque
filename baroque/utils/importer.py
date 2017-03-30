"""Utility functions for handling imports"""

import importlib


def class_from_dotted_path(dotted_path):
    """Loads a Python class from the supplied Python dot-separated class path.
    The class must be visible according to the PYTHONPATH variable contents.

    Example:
        ``"package.subpackage.module.MyClass" --> MyClass``

    Args:
        dotted_path (str): the dot-separated path of the class

    Returns:
        a ``type`` object

    """
    tokens = dotted_path.split('.')
    modpath, class_name = '.'.join(tokens[:-1]), tokens[-1]
    class_ = getattr(importlib.import_module(modpath), class_name)
    return class_
