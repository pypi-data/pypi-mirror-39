"""
Request Handler for the service dependency graph

"""
from tornado import web

from imbi import base


class RequestHandler(base.RequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('views/services/graph.html')
