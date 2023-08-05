"""
Request Handler for logged in home

"""
from tornado import web

from imbi import base


class RequestHandler(base.RequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.redirect('/services/inventory')
