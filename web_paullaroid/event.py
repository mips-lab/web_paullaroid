from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

import couchdb

@subscriber(ApplicationCreated)
def on_launch(event):
    couch = couchdb.Server(event.app.registry.settings.get('couchdb_url'))
    try:
        couch.create(event.app.registry.settings.get('couchdb_db'))
    except couchdb.http.PreconditionFailed:
        pass
