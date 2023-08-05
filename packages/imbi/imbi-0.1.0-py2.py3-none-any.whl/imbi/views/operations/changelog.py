"""
Request Handler for the Change Log

"""
from tornado import web

from imbi import base


class RequestHandler(base.RequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('views/operations/changelog.html')
