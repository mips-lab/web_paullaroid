from pyramid.config import Configurator
import couchdb


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)


    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('event', '/{event}/')
    config.add_route('image', '/{event}/{image}/')
    config.add_route('image_next', '/{event}/{image}/next')
    config.add_route('image_prev', '/{event}/{image}/prev')
    config.add_route('image_thumb', '/{event}/{image}/thumb/')
    config.add_route('image_raw', '/{event}/{image}/raw/')
    config.scan()

    couch = couchdb.Server(settings.get('couchdb_url'))
    db = couch[settings.get('couchdb_db')]

    def get_couchdb(request):
        return db

    config.add_request_method(get_couchdb, 'db', reify=True)
    return config.make_wsgi_app()
