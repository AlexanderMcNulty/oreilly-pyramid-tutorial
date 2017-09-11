from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from pyramid_sqlalchemy import metadata


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.scan()
    config.include('pyramid_sqlalchemy')
    metadata.create_all()
    config.add_static_view(name='deform_static', path='deform:static')
    config.add_static_view(name='static', path='mysite:static')
    config.add_route('home', '/')
    config.add_route('todo_list', '/todo')
    config.add_route('todo_add', '/todo/add')
    config.add_route('todo_view', '/todo/{id}')
    config.add_route('todo_edit', '/todo/{id}/edit')
    config.add_route('todo_delete', '/todo/{id}/delete')

    session_secret = settings['session.secret']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)

    return config.make_wsgi_app()
