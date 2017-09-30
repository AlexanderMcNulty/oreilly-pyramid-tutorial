from pyramid.config import Configurator
from pyramid_sqlalchemy import metadata


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')
    config.add_route('todos', '/api/todos')
    config.add_route('todo', '/api/todos/{id}',
                     factory='.models.todo_factory')
    config.scan()
    metadata.create_all()

    # Statically serve app directory at the "/" URL
    config.add_static_view(name='/', path='mysite:app')
    config.add_route('app_html', '/')

    return config.make_wsgi_app()
