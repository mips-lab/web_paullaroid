import glob
import os.path

from pyramid.view import view_config
from pyramid.response import FileResponse



@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    events_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'),'*')) #it's a gen 
    events = []
    for event in events_gen: 
        events.append(os.path.basename(event))
    
    return {'project': 'web_paullaroid', 'events': events}


@view_config(route_name='event', renderer='templates/event.pt')
def event_view(request):
    event_name = request.matchdict['event'] 
    
    images_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'),event_name, '*')) #it's a gen 
    images = []
    for image in images_gen: 
        images.append(os.path.basename(image))
    
    return {'event_name': event_name, 'images' : images}


@view_config(route_name='image', renderer='templates/image.pt')
def image_view(request):
    return {'image': request.matchdict.get('image'), 'event':
            request.matchdict.get('event')}


@view_config(route_name='image_raw')
def image_raw_view(request):
    event_name = request.matchdict['event'] 
    image_name = request.matchdict['image'] 
    path = os.path.join(request.registry.settings.get('directory'),event_name,
image_name)
    response = FileResponse(path, request=request)
#    reponse.content_disposition = u'attachment; filename="%s"' % image_name
    return response
