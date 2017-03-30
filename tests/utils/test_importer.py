from baroque.utils import importer


class Placeholder:
    pass


def test_class_from_dotted_path():
    path = 'tests.utils.test_importer.Placeholder'
    result = importer.class_from_dotted_path(path)
    assert result == Placeholder
