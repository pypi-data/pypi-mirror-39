"""
Transcoders for the sprockets.mixins.mediatype mixin

"""
import json

from sprockets.mixins.mediatype import handlers


class HTMLTranscoder(handlers.TextContentHandler):

    def __init__(self, content_type='text/html', default_encoding='utf-8'):
        super(HTMLTranscoder, self).__init__(
            content_type, self.dumps, self.loads, default_encoding)

    @staticmethod
    def dumps(value):
        """Just pass through the value if it's a string, otherwise dump it as
        JSON.

        :rtype: str

        """
        if not isinstance(value, (bytes, str)):
            value = '<html><body><pre>{}</pre></body></html>'.format(
                json.dumps(value, indent=2))
        return value

    @staticmethod
    def loads(value):
        """Just pass through the value."""
        return value
