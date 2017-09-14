from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    # this is where the js lives
    config.add_static_view(name='static', path='mysite:static')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
