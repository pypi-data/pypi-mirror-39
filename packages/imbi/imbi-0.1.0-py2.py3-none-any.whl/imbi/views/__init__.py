"""
Application Views

"""
from tornado import web

from . import error, home, operations, services

URLS = [
    web.url(r'/', home.RequestHandler),
] + operations.URLS + services.URLS
