from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

# check out @view_defaults to define a series of view functions that share a route
# but differ in another way for example by their request_method ie. GET, POST, DELETE, PUT

# classes are ideal for sharing state, computation, or other kinds of coupling

# when transitioning from view functions to a function class all the parameter we passed called request should change to self
class MySite:
    def __init__(self, request):
        self.request = request

    # using @property we don't have to call it with parenthesis in the template
    @property
    def current(self):
        return self.request.matchdict.get('id')

    @view_config(route_name='list',
                 renderer='templates/list.jinja2')
    def list(self):
        return dict()

    @view_config(route_name='add',
                 renderer='templates/add.jinja2')
    def add(self):
        return dict()

    @view_config(route_name='view',
                 renderer='templates/view.jinja2')
    def view(self):
        return dict()

    @view_config(route_name='edit',
                 renderer='templates/edit.jinja2')
    def edit(self):
        return dict()

    # the parameters passed to @view_config are all examples of predicates
    # what is an example of a custom predicate?
    @view_config(route_name='edit',
                 renderer='templates/edit.jinja2',
                 request_method='POST',
                 request_param='form.submit')
    def edit_handler(self):
        new_title = self.request.params.get('new_title')
        print('New title', new_title)
        url = self.request.route_url('list')
        return HTTPFound(url)

    @view_config(route_name='delete')
    def delete(self):
        url = self.route_url('list')
        return HTTPFound(url)
