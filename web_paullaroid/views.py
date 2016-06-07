import datetime
import glob
import os.path

from pyramid.view import view_config
from pyramid.response import FileResponse



@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    ''' home view
        parse dir in data, each dir is an event
    '''
    events_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'),'*')) #it's a gen
    events = []
    for event in events_gen:
        events.append(os.path.basename(event))

    return {'project': 'web_paullaroid', 'title': 'PauLLAroid' , 'events': events}


@view_config(route_name='event', renderer='templates/event.pt')
def event_view(request):
    ''' event view
        first visit just see only 10 newest pics,
        you can select date, to find specific pic
    '''
    date_post = request.GET.get('date_pict')
    event_name = request.matchdict['event']

    images_gen = glob.iglob(os.path.join(request.registry.settings.get('directory'), event_name, '*.jpg'))  # it's a gen
    images = []

    for image in images_gen:
        images.append(os.path.basename(image))

    images.sort(reverse=True)

    dates_tmp= {image.split('_')[0] for image in images}

    dates = [datetime.date(int(date.split('-')[0]),
                           int(date.split('-')[1]),
                           int(date.split('-')[2])) for date in dates_tmp]
    dates.sort(reverse=True)

    if date_post:
        images = [image for image in images if image.startswith(date_post)]

    else:
        images = images[:10]

    return {'title': event_name,
            'event_name': event_name,
            'images': images,
             'dates': dates}


@view_config(route_name='image', renderer='templates/image.pt')
def image_view(request):
    ''' image view
        see image with 100% of screen size
    '''
    return {'title': request.matchdict.get('event') + request.matchdict.get('image'),
            'image': request.matchdict.get('image'),
            'event_name':  request.matchdict.get('event')}


@view_config(route_name='image_thumb')
def image_thumb_view(request):
    ''' image thumb view
        see thumb of each picture (with  .thumbnail extension)
    '''
    event_name = request.matchdict['event']
    image_name = request.matchdict['image']
    path = os.path.join(request.registry.settings.get('directory'),
                        event_name,
                        image_name+".thumbnail")
    response = FileResponse(path, request=request)
#    reponse.content_disposition = u'attachment; filename="%s"' % image_name
    return response


@view_config(route_name='image_raw')
def image_raw_view(request):
    ''' image raw view
        see raw of each picture
    '''
    event_name = request.matchdict['event']
    image_name = request.matchdict['image']
    path = os.path.join(request.registry.settings.get('directory'),
                        event_name,
                        image_name)
    response = FileResponse(path, request=request)
#    reponse.content_disposition = u'attachment; filename="%s"' % image_name
    return response
