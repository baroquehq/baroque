import pytz
import datetime

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
"""str: ISO-8601 time format used for timestamp printing"""


def utc_now():
    """Gives the current UTC time-aware timestamp.

    Returns:
        `datetime.datetime`: The UTC timestamp

    """
    ts = datetime.datetime.utcnow()
    return ts.replace(tzinfo=pytz.utc)


def stringify(timestamp):
    """Turns a timestamp into its ISO-8601 string representation.

    Note:
        refer to the `TIME_FORMAT` template string

    Args:
        timestamp (:obj:`datetime.datetime`): the timestamp to be stringified

    Returns:
        str: The ISO-8601 time formatted string

    """
    return timestamp.strftime(TIME_FORMAT)
