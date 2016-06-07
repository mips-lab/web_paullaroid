import glob
import json
import os.path

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

    db = couch[event.app.registry.settings.get('couchdb_db')]

    for view in glob.glob(os.path.join(os.path.dirname(__file__), 'data', '*.js')):
        with open(view, 'rb') as current:
            doc = json.load(current)
            db.save(doc)
