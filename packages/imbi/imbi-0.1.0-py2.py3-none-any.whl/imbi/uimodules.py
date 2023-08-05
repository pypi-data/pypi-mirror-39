from tornado import web


class Table(web.UIModule):

    def render(self, data, header=True):
        return self.render_string(
            'modules/table.html', data=data, header=header)


class Value(web.UIModule):

    def render(self, value, key=None):
        link = None
        if key == 'link':
            link = value
        elif isinstance(value, str) and value.startswith('http'):
            link = value
        return self.render_string(
            'modules/value.html', value=value, key=key, link=link)
