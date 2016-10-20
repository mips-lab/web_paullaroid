import datetime
import os.path

from pyramid.view import view_config
from pyramid.response import FileResponse



@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    ''' home view
        parse dir in data, each dir is an event
    '''

    events = request.db.view('_design/images/_view/all', reduce=True,
                             group_level=1)


    return {'project': 'web_paullaroid', 'title': 'PauLLAroid',
            'events': [row for row in events]}


@view_config(route_name='event', renderer='templates/event.pt')
def event_view(request):
    ''' event view
        first visit just see only 10 newest pics,
        you can select date, to find specific pic
    '''
    selected_date = request.GET.get('date_pict')
    event_name = request.matchdict['event']


    if selected_date:
        images = request.db.view('_design/images/_view/all', reduce=False,
                                  start_key=[event_name, selected_date],
                                  end_key=[event_name, selected_date, {}])
    else:
        images = request.db.view('_design/images/_view/all', reduce=False,
                                  start_key=[event_name],
                                  end_key=[event_name, {}])

        images = [image for image in images][:10]


    dates = request.db.view('_design/images/_view/all', reduce=True,
                             start_key=[event_name],
                             end_key=[event_name, {}],
                             group_level=2)

    return {'title': event_name,
            'event_name': event_name,
            'images': [image.id for image in images],
             'dates': [datetime.datetime.strptime(date.key[1], '%Y-%m-%d').date() for date in dates]}


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
