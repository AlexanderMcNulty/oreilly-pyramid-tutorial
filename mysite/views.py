from pyramid.view import view_config


class MySite:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='templates/home.jinja2')
    def home(self):
        return dict()

    @view_config(route_name='home', renderer='json', request_method='POST')
    def greeting(self):
        # request.params vs request.json_body
        # to learn more read "Dealing with a JSON-encoded request body"
        # browser now sends and returns json
        greeting = 'Hello %s!' % self.request.json_body.get('name')
        return dict(greeting=greeting)


    '''
    # renderer user to pass templates, now we can use it to pass json
    # passing data will change the response headers
    @view_config(route_name='greeting', renderer='json')
    def greeting(self):
        # request.params vs request.json_body
        # to learn more read "Dealing with a JSON-encoded request body"
        # browser now sends and returns json
        greeting = 'Hello %s!' % self.request.json_body.get('name')
        return dict(greeting=greeting)
    '''
