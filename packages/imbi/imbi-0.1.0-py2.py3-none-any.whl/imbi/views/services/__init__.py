"""
Services Views

"""
from tornado import web

from . import graph, inventory

URLS = [
    web.url(r'/services/graph', graph.RequestHandler),
    web.url(r'/services/inventory', inventory.RequestHandler)
]
