from pyramid.config import Configurator
from pyramid_sqlalchemy import metadata

# new focus on the application not the serving of our application


# this code has been removed from __init__.py into views.py
# this makes the purpose this file more clear, the bootstrapping of the application
# which i think means configure
'''
from pyramid.view import view_config

@view_config(route_name='list', renderer='list.jinja2')
def list(request):
    return dict()
'''


# entry point tells us to come here, to main.
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_sqlalchemy')
    # below is "asset specifications", packagename:pathtoasset (in this case the name of our static directory)
    # this is awesome because as long as we know our package name and don't modify their directory stree
    # then we never need to change the path regardless of where our package is used.
    config.add_static_view(name='static', path='mysite:static')
    config.add_route('home', '/')
    config.add_route('todo_list', '/todos')
    config.add_route('todo_add', '/todos/add')
    config.add_route('todo_view', '/todos/{id}')
    config.add_route('todo_edit', '/todos/{id}/edit')
    config.add_route('todo_delete', '/todos/{id}/delete')
    config.scan()
    # go and register all of our models with our sqlalchemy object relational mapper.
    # create is done last in order to give packages time to import.
    # object Metadata was passed in by the sqlalchemy package
    metadata.create_all()
    return config.make_wsgi_app()
