"""
Request Handler for the services inventory

"""
from tornado import web

from imbi import base


class RequestHandler(base.RequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('views/services/inventory.html')
