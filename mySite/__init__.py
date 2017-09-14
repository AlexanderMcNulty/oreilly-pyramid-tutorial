from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('greeting', '/greeting')
    config.scan()

    # Statically serve app directory at the "/" URL
    config.add_route('app_html', '/')
    config.add_static_view(name='/', path='mysite:app')

    return config.make_wsgi_app()
