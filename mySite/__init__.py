from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from pyramid_sqlalchemy import metadata

# convert credentials into principles
from .security import groupfinder

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.scan()
    config.include('pyramid_sqlalchemy')
    metadata.create_all()
    config.add_static_view(name='deform_static', path='deform:static')
    config.add_static_view(name='static', path='mysite:static')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # Todo routes with route factory
    config.add_route('todos_list', '/todos',
                     factory='.models.todos.todo_factory') # dotted path
    config.add_route('todos_add', '/todos/add',
                     factory='.models.todos.todo_factory')
    config.add_route('todos_view', '/todos/{id}',
                     factory='.models.todos.todo_factory')
    config.add_route('todos_edit', '/todos/{id}/edit',
                     factory='.models.todos.todo_factory')
    config.add_route('todos_delete', '/todos/{id}/delete',
                     factory='.models.todos.todo_factory')

    session_secret = settings['session.secret']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    return config.make_wsgi_app()
