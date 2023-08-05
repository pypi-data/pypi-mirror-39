"""
Base Request Handlers

"""
import logging
from email import utils
import traceback

from sprockets.mixins import correlation, mediatype, sentry
from tornado import web

from imbi import session, timestamp, __version__

LOGGER = logging.getLogger(__name__)


class RequestHandler(sentry.SentryMixin,
                     correlation.HandlerMixin,
                     mediatype.ContentMixin,
                     web.RequestHandler):
    """Base RequestHandler class used for recipients and subscribers."""

    def __init__(self, application, request, **kwargs):
        self._error = None
        self.logger = None
        self.session = None
        super(RequestHandler, self).__init__(application, request, **kwargs)

    def initialize(self):
        """Hook for subclass initialization. Called for each request.

        A dictionary passed as the third argument of a url spec will be
        supplied as keyword arguments to initialize().

        """
        super(RequestHandler, self).initialize()
        self.logger = logging.LoggerAdapter(
            LOGGER, {'correlation-id': self.correlation_id})

    async def prepare(self):
        """Prepare the request handler for the request. If the application
        is not ready return a ``503`` error.

        Checks for a session cookie and if present, loads the session into
        the current user and authenticates it. If authentication fails,
        the current user and cookie is cleared.

        """
        if not self.application.ready_to_serve:
            return self.send_error(503, reason='Application not ready')
        self.session = session.Session(self)
        await self.session.initialize()
        return super(RequestHandler, self).prepare()

    def compute_etag(self):
        """Override Tornado's built-in ETag generation"""
        return None

    def get_current_user(self):
        """Used by the system to manage authentication behaviors.

        :rtype: imbi.session.User or None

        """
        if self.session:
            return self.session.user

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        The results of this method will be combined with additional defaults
        in the :py:module:`tornado.template` module and keyword arguments to
        :py:meth:`~tornado.web.RequestHandler.render`
        or :py:meth:`~tornado.web.RequestHandler.render_string`.

        """
        namespace = super(RequestHandler, self).get_template_namespace()
        namespace.update({'__version__': __version__})
        return namespace

    def set_default_headers(self):
        """Override the default headers, setting the Server response header"""
        super(RequestHandler, self).set_default_headers()
        self.set_header('Server', '{}/{}'.format('admin', __version__))

    def write_error(self, status_code, **kwargs):
        """Implements custom error responses in a restful fashion that returns
        HTML to browsers, but machine readable responses to API clients.

        write_error may call write, render, set_header, etc to produce output
        as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an exc_info triple will be available as kwargs["exc_info"].
        Note that this exception may not be the “current” exception for
        purposes of methods like sys.exc_info() or traceback.format_exc.

        :param int status_code: The status code of the error
        :param dict kwargs: sys.exec_info() like arguments

        """
        content_type = self.get_response_content_type()
        response = {'type': status_code,
                    'message': self._reason,
                    'traceback': None}
        if self.settings['debug']:
            response['traceback'] = \
                [l.strip() for l in
                 traceback.format_exception(*kwargs['exc_info'])
                 if l.strip()][1:]
        if content_type.startswith('text/html'):
            return self.render('views/error.html', **response)
        self.send_response(response)

    def _add_date_header(self, value):
        """Add a RFC-822 formatted timestamp for the Date HTTP response header.

        :param str value: The value to set the Date header to

        """
        self.set_header('Date', self._rfc822_date(value))

    def _add_etag_header(self, record_type, record_version):
        """Adds the entity tag response header

        :param str record_type: The type of record being returned
        :param int record_version: The version of the record

        """
        self.add_header('Etag', '{}/{}'.format(record_type, record_version))

    def _add_last_modified_header(self, value):
        """Add a RFC-822 formatted timestamp for the Last-Modified HTTP
        response header.

        :param str value: The value to set the Date header to

        """
        self.set_header('Last-Modified', self._rfc822_date(value))

    def _add_version_header(self, value):
        """Add a Version HTTP Header.

        :param str value: The value to set the Version header to

        """
        self.set_header('Version', value)

    def _add_link_header(self, record_type, record_id):
        """Adds the Link response header

        :param str record_type: The type of record being returned
        :param str record_id: The version of the record

        """
        self.add_header('Link', '<{}>; rel="self"'.format(
            self.reverse_url(record_type, record_id)))

    def _add_response_caching_headers(self, ttl):
        """Adds the cache response headers for the object being returned.

        :param int ttl: The time-to-live for the caching header

        """
        self.add_header('Cache-Control', 'public, max-age={}'.format(ttl))

    def _check_preconditions(self, record):
        """Checks for supported preconditions in the request headers and
        raise an error if they fail.

        :param dict record: The record to check
        :raises: web.HTTPError

        """
        ius_value = self.get_request_header('If-Unmodified-Since', None)
        if not ius_value:
            return
        unmodified_since = timestamp.parse_rfc822(ius_value)
        if not unmodified_since:
            self.logger.info('Invalid If-Unmodified-Since: %r', ius_value)
            return

        last_write = record.get('_modified_at') or record.get('_created_at')
        if last_write:
            modified_at = timestamp.parse(last_write)
            if modified_at >= unmodified_since:
                raise web.HTTPError(
                    412, 'Last modified at {}'.format(modified_at.isoformat()))

    @property
    def _no_cache(self):
        """Returns True if a client has sent a header asking for a non-cached
        version of an object.

        :rtype: bool

        """
        return self.request.headers.get('Pragma') == 'no-cache'

    @staticmethod
    def _rfc822_date(value):
        """Return an RFC-822 formatted timestamp for the given ISO-8601
        timestamp.

        :param str value: The ISO-8601 value
        :rtype: str

        """
        return utils.format_datetime(timestamp.parse(value))
