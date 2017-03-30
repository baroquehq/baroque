import os
import pytest
from baroque.utils import configreader
from baroque.exceptions.configuration import ConfigurationNotFoundError, \
    ConfigurationParseError


def test_readconfig():
    # path is not a regulare file
    with pytest.raises(ConfigurationNotFoundError):
        configreader.readconfig('abcdefgh')
        pytest.fail()

    # path is a regular file, but not YML
    this_file = os.path.realpath(__file__)
    with pytest.raises(ConfigurationParseError):
        configreader.readconfig(this_file)
        pytest.fail()

    # config is read OK
    this_dir = os.path.dirname( __file__ )
    yml_file = os.path.join(os.path.dirname(os.path.dirname(this_dir)),
                            'baroque.yml')
    conf = configreader.readconfig(yml_file)
    assert isinstance(conf, dict)


def test_read_config_or_default():
    # returning default config
    assert isinstance(configreader.read_config_or_default(None), dict)

    # calling configreader.readconfig function
    with pytest.raises(ConfigurationNotFoundError):
        configreader.readconfig('abcdefgh')
        pytest.fail()
