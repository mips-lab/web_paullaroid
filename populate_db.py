import couchdb
import glob
import os

couch = couchdb.Server('http://couchdb.paulla.asso.fr')

db = couch['paullaroid']


events_gen = glob.iglob(os.path.join('data','*')) #it's a

for event in events_gen:
    doc = { '_id' : os.path.basename(event), 'type_doc':'event'}

    db.save(doc)
    pict_gen = glob.iglob(os.path.join(event,'*.jpg'))
    for pict in pict_gen:
        picture = { '_id' : os.path.basename(pict), 'type_doc':'image',
                    'datetime': ' '.join(os.path.basename(pict).split('_')[:-1]),
                    'event_id': os.path.basename(event)}

        db.save(picture)
        with open(pict, 'rb') as current_pict_full:
            db.put_attachment(picture, current_pict_full, filename='full',
                              content_type='image/jpeg')


        with open(pict+'.thumbnail', 'rb') as current_pict_thumb:
            db.put_attachment(picture, current_pict_thumb, filename='thumb',
                              content_type='image/jpeg')
