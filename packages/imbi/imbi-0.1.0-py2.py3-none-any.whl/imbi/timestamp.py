"""
Handy Timestamp Methods

"""
import datetime
from email import utils

import arrow
from dateutil import tz


def age(value):
    """Return the age of a timestamp as a datetime.timedelta

    :rtype: datetime.timedelta

    """
    return arrow.utcnow() - arrow.get(value)


def isoformat(value=None):
    """Format a datetime Object as an ISO-8601 timestamp without milliseconds.
    If the value is not returned, return the current time in UTC.

    :param datetime.datetime value: The optional value to format
    :rtype: str

    """
    if not value:
        value = datetime.datetime.now(tz=tz.tzoffset(None, 0))
    output = value.isoformat(' ')
    if '.' in output:
        parts = output.split('.')
        return '{}{}'.format(parts[0], parts[1][6:])
    return output


def parse(value):
    """Parse an ISO-8601 formatted timestamp

    :param str value: The timestamp to parse
    :rtype: datetime.datetime

    """
    return arrow.get(value).datetime


def parse_rfc822(value):
    """Parse an RFC-822 formatted timestamp value, returning a
    :py:class:`~datetime.datetime` instance.

    :param str value: RFC-822 formatted timestamp value
    :rtype: datetime.datetime

    """
    parsed = utils.parsedate_tz(value)
    if not parsed:
        return None
    return datetime.datetime.fromtimestamp(
        utils.mktime_tz(parsed), tz.tzoffset(None, 0))


def to_utc(value):
    """Convert an ISO-8601 formatted timestamp to UTC.

    :param  str value: The timestamp to parse
    :rtype: str

    """
    return isoformat(arrow.get(value).to('UTC'))
