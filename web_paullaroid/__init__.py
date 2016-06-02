from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

 #   config.registry.settings = settings

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('event', '/{event}/')
    config.add_route('image', '/{event}/{image}/')
    config.add_route('image_thumb', '/{event}/{image}/thumb/')
    config.add_route('image_raw', '/{event}/{image}/raw/')
    config.scan()
    return config.make_wsgi_app()
