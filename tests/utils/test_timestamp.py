import datetime
from baroque.utils import timestamp


def test_utc_now():
    utc_ts = timestamp.utc_now()
    assert utc_ts.tzinfo is not None


def test_stringify():
    dateobj = datetime.datetime(1983, 7, 3, 9, 0, 0)
    result = timestamp.stringify(dateobj)
    assert isinstance(result, str)
