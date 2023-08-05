"""
Core Application
================

"""
import logging
import os
from os import path
import sys

from sprockets import http
from sprockets.handlers import status
from sprockets.mixins import sentry
from sprockets.mixins.mediatype import content, transcoders
from tornado import web

from imbi import auth, common, html, pkgfiles, uimodules, views, __version__

LOGGER = logging.getLogger(__name__)

REQUEST_LOG_FORMAT = '%d %s %.2fms %s'


def make_application(**settings):
    """Create the web application instance after building the settings

    :param dict settings: kwarg settings passed in for the application
    :rtype: imbi.app.Application

    """
    _set_default_settings(settings)
    if settings['environment'] in ('development', 'testing'):
        os.environ.pop('SENTRY_DSN', None)
        settings.setdefault('debug', True)
    status.set_application(str(settings['service']))

    urls = [
        web.url(r'/login', auth.LoginHandler),
        web.url(r'/logout', auth.LogoutHandler),
        web.url(r'/static/(.*)', web.StaticFileHandler,
                {'path': settings['static_path']}),
        web.url(r'/status', status.StatusHandler)
    ]
    urls += views.URLS

    app = Application(urls, **settings)

    # Content handling setup
    content.set_default_content_type(app, 'application/json')
    content.add_transcoder(app, transcoders.JSONTranscoder())
    content.add_transcoder(app, transcoders.MsgPackTranscoder())
    content.add_transcoder(app, html.HTMLTranscoder())

    # Instrument which libraries to include in sentry tracebacks
    sentry.install(
        app,
        include_paths=[
            'arrow',
            'imbi',
            'jsonpatch',
            'jsonschema',
            'sprockets_influxdb',
            'sprockets.http',
            'sprockets.handlers.status',
            'sprockets.mixins.correlation',
            'sprockets.mixins.mediatype',
            'sprockets.mixins.metrics',
            'sprockets.mixins.sentry'],
        release=__version__,
        tags={'environment': settings['environment']})
    return app


def _maybe_disable_request_logging():
    """Adjust logging levels, turning off access logging in production."""
    for name in {'imbi', 'tornado'}:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
    if os.environ.get('DEBUG') == '1':
        for name in {'imbi'}:
            logging.getLogger(name).setLevel(logging.DEBUG)


def _set_default_settings(settings):
    """Update the settings, setting default values that will not override
    any previous configuration.

    :param dict settings: Application settings preset values
    :rtype: dict

    """
    settings.setdefault('compress_response', False)
    settings.setdefault('cookie_secret',  os.environ.get(
        'COOKIE_SECRET', common.DEFAULT_COOKIE_SECRET))
    settings.setdefault('default_handler_class', views.error.RequestHandler)
    settings.setdefault(
        'environment', os.environ.get('ENVIRONMENT', 'development'))
    settings.setdefault('debug', False)
    settings.setdefault('login_url', '/login')
    settings.setdefault(
        'redis_url', os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
    settings.setdefault('service', os.environ.get('SERVICE', 'imbi'))
    settings.setdefault(
        'static_path',
        path.join(path.dirname(sys.modules['imbi'].__file__), 'static'))
    settings.setdefault(
        'template_loader',
        pkgfiles.TemplateLoader(debug=settings.get('debug', False)))
    settings.setdefault('template_path', 'templates')
    settings.setdefault('ui_modules', uimodules)
    settings.setdefault('version', __version__)
    settings.setdefault('xheaders', True)
    settings.setdefault('xsrf_cookie', True)


class Application(web.Application):
    """Extend tornado.web.Application to create our various client objects and
    to implement the ready_to_serve logic.

    """
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self._access_log = logging.LoggerAdapter(
            logging.getLogger('tornado.access'), {'correlation-id': ''})
        self.redis = None

    @property
    def environment(self):
        """Return the operational environment as a string

        :rtype: str

        """
        return self.settings['environment']

    def log_request(self, handler):
        """Writes a completed HTTP request to the logs.
        By default writes to the python root logger.

        """
        status_code = handler.get_status()
        if status_code < 400:
            log_method = self._access_log.info
        elif status_code < 500:
            log_method = self._access_log.warning
        else:
            log_method = self._access_log.error
        request_time = 1000.0 * handler.request.request_time()
        correlation_id = getattr(handler, 'correlation_id', None)
        if correlation_id is None:
            correlation_id = handler.request.headers.get(
                'Correlation-ID', None)
        self._access_log.extra['correlation-id'] = correlation_id
        log_method(REQUEST_LOG_FORMAT, status_code,
                   handler._request_summary(), request_time,
                   handler.request.headers.get('User-Agent'))

    @property
    def ready_to_serve(self):
        """Indicates if the service is available to respond to HTTP requests.

        :rtype bool

        """
        return True

    @property
    def status(self):
        """Expose the application status, indicating if it is ready to serve.

        :rtype: str

        """
        return 'ok' if self.ready_to_serve else status.MAINTENANCE


def run():  # pragma: no cover
    """Run the service"""
    number_of_procs = os.environ.get('NUMBER_OF_PROCS')
    if number_of_procs:
        http.run(make_application, {'number_of_procs': int(number_of_procs)})
    else:
        http.run(make_application)
