from pyramid.view import view_config
import glob
import os.path

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    events_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'),'*')) #it's a gen 
    events = []
    for event in events_gen: 
        events.append(os.path.basename(event))
    
    return {'project': 'web_paullaroid', 'events': events}


@view_config(route_name='image', renderer='templates/image.pt')
def image_view(request):
    return {'image': request.matchdict.get('image'), 'event':
    request.matchdict.get('event')}


@view_config(route_name='event', renderer='templates/event.pt')
def event_view(request):
    event_name = request.matchdict['event'] 
    
    images_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'),event_name, '*')) #it's a gen 
    images = []
    for image in images_gen: 
        images.append(os.path.basename(image))
    
    return {'event_name': event_name, 'images' : images}
