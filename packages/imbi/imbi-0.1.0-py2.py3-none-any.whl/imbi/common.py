"""
Common methods and constants

"""
import os
import re

from tornado import web

DEFAULT_COOKIE_SECRET = 'imbi'
SIGNED_VALUE_PATTERN = re.compile(r'^(?:[1-9][0-9]*)\|(?:.*)$')


def is_encrypted_value(value):
    """Checks to see if the value matches the format for a signed value using
    Tornado's signing methods.

    :param str value: The value to check
    :rtype: bool

    """
    if value is None or not isinstance(value, str):
        return False
    return SIGNED_VALUE_PATTERN.match(value) is not None


def encrypt_value(key, value):
    """Encrypt a value using the code used to create Tornado's secure cookies,
    using the common cookie secret.

    :param str key: The name of the field containing the value
    :param str value: The value to encrypt
    :rtype: str

    """
    return web.create_signed_value(
        os.environ.get('COOKIE_SECRET', DEFAULT_COOKIE_SECRET),
        key, value).decode('utf-8')


def decrypt_value(key, value):
    """Decrypt a value that is encrypted using Tornado's secure cookie
    signing methods.

    :param str key: The name of the field containing the value
    :param str value: The value to decrypt
    :rtype: str

    """
    return web.decode_signed_value(
        os.environ.get('COOKIE_SECRET', DEFAULT_COOKIE_SECRET), key, value)
