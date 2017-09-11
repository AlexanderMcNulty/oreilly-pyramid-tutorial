from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, notfound_view_config

import colander
from deform import Form, ValidationFailure

# Session is a convention used by pyramid_sqlalchemy to access underlying mechanisms
from pyramid_sqlalchemy import Session

from .models import ToDo

class ToDoItem(colander.MappingSchema):
    # our schema says that the title is a string
    # if our schema has title as an integer then the appstruct will convert the forms string to an integer
    title = colander.SchemaNode(colander.String())


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
        self.messages = request.session.pop_flash()

    # using @property we don't have to call it with parenthesis in the template
    @property
    def current(self):
        todo_id = int(self.request.matchdict.get('id'))
        todo = Session.query(ToDo).filter_by(id=todo_id).one()
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
        todos = Session.query(ToDo).order_by(ToDo.title)
        # old static way of passings data to client
        # msg = self.request.params.get('msg')
        return dict(
            todos=todos
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
            # form NOT valid
            return dict(add_form=e.render())
        # new_title =  self.request.params.get('title')
        # because we have an appstruct we can get the new title from the appstruct
        # instead of using the self.request.params.get('title')
        title = appstruct['title']
        Session.add(ToDo(title=title))
        todo = Session.query(ToDo).filter_by(title=title).one()
        self.request.session.flash('Added: %s' % todo.id)
        url = self.request.route_url('todo_list',
                                     id=todo.id
                                     )
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
        # deform wants a dictionary but sqlalchemy returns an object
        edit_form = self.form.render(dict(title=self.current.title))
        return dict(todo=self.current, edit_form=edit_form)

    # the parameters passed to @view_config are all examples of predicates
    # what is an example of a custom predicate?
    # removed, request_param='form.submit', deform takes care of this for us.
    @view_config(route_name='todo_edit',
                 renderer='templates/edit.jinja2',
                 request_method='POST')
    def edit_handler(self):
        controls = self.request.POST.items()
        try:
            appstruct = self.form.validate(controls)
        except ValidationFailure as e:
            # form is NOT valid
            return dict(edit_form=e.render())

        # Valid form so save the title and redirect with message
        self.current.title = appstruct['title']
        # is this equivalent? /\ vs \/
        # self.current['title'] = new_title
        self.current.title = appstruct['title']
        self.request.session.flash('Changed: %s' % self.current.id)
        url = self.request.route_url('todo_view',
                                     id=self.current.id)
        return HTTPFound(url)

    @view_config(route_name='todo_delete')
    def delete(self):
        msg = 'Deleted: %s' % (self.current.id)
        self.request.session.flash('Deleted: %s' % self.current.id)
        Session.delete(self.current)
        url = self.request.route_url('todo_list',
                             _query=dict(msg=msg))
        return HTTPFound(url)
