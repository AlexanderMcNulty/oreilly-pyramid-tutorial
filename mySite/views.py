from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, notfound_view_config

import colander
from deform import Form, ValidationFailure


class ToDoItem(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())


sample_todos = {
    '1': dict(id='1', title='get milk'),
    '2': dict(id='2', title='get eggs')
}

# - check out @view_defaults to define a series of view functions that share a route
# - but differ in another way for example by their request_method ie. GET, POST, DELETE, PUT
# - classes are ideal for sharing state, computation, or other kinds of coupling
# - when transitioning from view functions to a function class all the parameter we passed called request should change to self


class MySite:
    def __init__(self, request):
        self.request = request
        self.schema = ToDoItem()
        self.form = Form(self.schema, buttons=('submit',))
        # extract a message from the url and assign it to the view
        # the html for this is being moved into the base template so 'msg' must exist for every template
        # therefore we can not do this in the 'lazy' @property fashion
        self.msg = request.params.get('msg')


    # using @property we don't have to call it with parenthesis in the template
    @property
    def current(self):
        todo_id = self.request.matchdict.get('id')
        todo = sample_todos.get(todo_id)
        if not todo:
             raise HTTPNotFound()
        return todo


    @notfound_view_config(renderer='templates/notfound.jinja2')
    def not_found(self):
        return dict()

    @view_config(route_name='home', renderer='templates/home.jinja2')
    def go_home(self):
        return dict()

    @view_config(route_name='todo_list',
                 renderer='templates/list.jinja2')
    def list(self):
        # if message was found extract and provide it to the template
        msg = self.request.params.get('msg')
        return dict(
            todos=sample_todos.values(),
            msg=msg
        )

    @view_config(route_name='todo_add',
                 renderer='templates/add.jinja2')
    def add(self):
        return dict(add_form=self.form.render())

    @view_config(route_name='todo_add',
                 renderer='templates/add.jinja2',
                 request_method='POST')
    def add_handler(self):
        controls = self.request.POST.items()
        try:
            appstruct = self.form.validate(controls)
        # if processing the form results in a validation error then return the form with an error message
        except ValidationFailure as e:
            return dict(add_form=e.render())
        # new_title =  self.request.params.get('title')
        # because we have an appstruct we can get the new title from the appstruct
        # instead of using the self.request.params.get('title')
        title = appstruct['title']
        msg = 'new_title: ' + title
        url = self.request.route_url('todo_list', _query={'msg': msg})
        return HTTPFound(url)

    @view_config(route_name='todo_view',
                 renderer='templates/view.jinja2')
    def view(self):
        # if self.current != '1':
        # pyramid exception that we imported
        # raising instead of returning is helpful if you are several levels into a program
            # raise HTTPNotFound()
        return dict(todo=self.current)

    @view_config(route_name='todo_edit',
                 renderer='templates/edit.jinja2')
    def edit(self):
        edit_form = self.form.render(self.current)
        return dict(todo=self.current, edit_form=edit_form)

    # the parameters passed to @view_config are all examples of predicates
    # what is an example of a custom predicate?
    # removed, request_param='form.submit', deform takes care of this for us.
    @view_config(route_name='todo_edit',
                 renderer='templates/edit.jinja2',
                 request_method='POST')
    def edit_handler(self):
        new_title = self.request.params.get('title')
        self.current['title'] = new_title
        msg = 'new_title: ' + new_title
        url = self.request.route_url('todo_list', _query={'msg':msg})
        return HTTPFound(url)

    @view_config(route_name='todo_delete')
    def delete(self):
        url = self.route_url('todo_list')
        return HTTPFound(url)
