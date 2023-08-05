"""
Request Handler used for rendering errors

"""
from tornado import web

from imbi import base


class RequestHandler(base.RequestHandler):

    def get(self, *args, **kwargs):
        raise web.HTTPError(404, 'File Not Found')
