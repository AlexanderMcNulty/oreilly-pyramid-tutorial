import os

from pyramid.response import FileResponse
from pyramid.view import view_config


class MySite:
    def __init__(self, request):
        self.request = request
        here = os.path.dirname(__file__)
        self.index_path = os.path.join(here, 'app', 'index.html')

    @view_config(route_name='app_html')
    def index_view(self):
        return FileResponse(self.index_path, request=self.request)

    @view_config(route_name='greeting', renderer='json')
    def greeting(self):
        greeting = 'Hello %s!' % self.request.json_body.get('name')
        return dict(greeting=greeting)
