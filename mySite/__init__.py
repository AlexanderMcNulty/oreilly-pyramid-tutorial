from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from pyramid_sqlalchemy import metadata

# convert credentials into principles
from .security import groupfinder

def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='.resources.Root')
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
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

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
