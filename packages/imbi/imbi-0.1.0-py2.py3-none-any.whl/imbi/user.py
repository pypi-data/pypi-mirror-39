"""
User Model for LDAP data

"""
import datetime
import logging

from imbi import common, ldap, timestamp

LOGGER = logging.getLogger(__name__)


class User:
    """Holds the user attributes and interfaces with the directory server"""

    REFRESH_AFTER = datetime.timedelta(minutes=5)

    def __init__(self, username=None, password=None):
        self._ldap = ldap.Client()
        self._conn = None
        self.cn = None
        self.dn = None
        self.email = None
        self.given_name = None
        self.groups = []
        self.initials = None
        self.last_refreshed_at = None
        self.name = None
        self.ou = None
        self.password = password
        self.surname = None
        self.title = None
        self.username = username

    def __setattr__(self, name, value):
        """Intercept the assignment of a signed password and decrypt it
        if it appears to be encrypted.

        :param str name: The attribute name that is being set
        :param mixed value: The attribute value being assigned

        """
        if name == 'password' and common.is_encrypted_value(value):
            value = common.decrypt_value(name, value)
        object.__setattr__(self, name, value)

    def as_dict(self):
        """Return a representation of the user data as a dict.

        :rtype: dict

        """
        return {
            'cn': self.cn,
            'dn': self.dn,
            'email': self.email,
            'given_name': self.given_name,
            'groups': self.groups,
            'initials': self.initials,
            'last_refreshed_at': self.last_refreshed_at,
            'name': self.name,
            'ou': self.ou,
            'password': common.encrypt_value('password', self.password),
            'surname': self.surname,
            'title': self.title,
            'username': self.username
        }

    async def authenticate(self):
        """Validate that the current session is still valid. Returns boolean
        if successful.

        :rtype: boolean

        """
        self._conn = await self._ldap.connect(self.username, self.password)
        if self._conn:
            LOGGER.debug('Authenticated as %s', self.username)
            if not self.dn:
                result = self._conn.extend.standard.who_am_i()
                self.dn = result[3:].strip()
                await self.refresh()
            return True
        return False

    async def refresh(self):
        """Update the attributes from LDAP"""
        LOGGER.debug('Refreshing attributes from LDAP server')
        attrs = await self._ldap.attributes(self._conn, self.dn)
        self.cn = str(attrs.cn)
        self.email = str(attrs.mail)
        self.given_name = str(attrs.givenName)
        self.groups = await self._ldap.groups(self._conn, self.dn)
        self.initials = str(attrs.initials)
        self.last_refreshed_at = timestamp.isoformat()
        self.name = str(attrs.displayName)
        self.ou = str(attrs.ou)
        self.surname = str(attrs.sn)
        self.title = str(attrs.title)

    @property
    def should_refresh(self):
        """Returns True if the amount of time that has passed since the last
        refresh has exceeded the threshold.

        :rtype: bool

        """
        return self.REFRESH_AFTER < timestamp.age(self.last_refreshed_at)
