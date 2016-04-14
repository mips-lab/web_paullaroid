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


