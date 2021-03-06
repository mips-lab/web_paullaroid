import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


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
    selected_hour = request.GET.get('hour_pict')
    event_name = request.matchdict['event']



    dates = request.db.view('_design/images/_view/all', reduce=True,
                             start_key=[event_name],
                             end_key=[event_name, {}],
                             group_level=2)

    if selected_date:
        images = request.db.view('_design/images/_view/all', reduce=False,
                                  end_key=[event_name, selected_date],
                                  start_key=[event_name, selected_date, {}],
                                  descending=True)

    else:
        images = request.db.view('_design/images/_view/all', reduce=False,
                                  end_key=[event_name],
                                  start_key=[event_name, {}], 
                                  descending=True)
    

    hours = []
    for image in images:
        hour = image.id.split('_')[1].split('-')[0]
        hours.append(hour)

    hours = list(set(hours))
    hours = [ int(hour.decode('utf-8')) for hour in hours]
    hours.sort()
    hours.insert(0, 'all')

    #import pdb; pdb.set_trace()
    
    images_new = []
    if type(selected_hour) == type(int()):
        for image in images:
            hour_image = image.id.split('_')[1].split('-')[0]
            if hour_image == selected_hour:
                images_new.append(image)
        images = images_new
    

    image2 = []
    imlist = []
    images = list(images)
    for image in images:
        image2.append(image.id)
        if (images.index(image) +1) % 4 == 0:
            imlist.append(image2)
            image2 = list()
            

    return {'title': event_name,
            'event_name': event_name,
            'images': imlist,
             'dates': [datetime.datetime.strptime(date.key[1], '%Y-%m-%d').date() for date in dates],
             'hours': hours}

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
    image_name = request.matchdict['image']
    response = request.response

    if request.registry.settings.get('x-accel', 'false').lower() == 'true':
        headers = response.headers
        headers['X-Accel-Redirect'] =  str('/couch/%s/thumb' % image_name)
    else:
        image = request.db.get_attachment(image_name, 'thumb')
        response.body_file = image
        response.content_type = 'image/jpeg'
    return response


@view_config(route_name='image_raw')
def image_raw_view(request):
    ''' image raw view
        see raw of each picture
    '''
    image_name = request.matchdict['image']
    response = request.response

    if request.registry.settings.get('x-accel', 'false').lower() == 'true':

        headers = response.headers
        headers['X-Accel-Redirect'] =  str('/couch/%s/full' % image_name)
    else:
        image = request.db.get_attachment(image_name, 'full')
        response.body_file = image
        response.content_type = 'image/jpeg'

    return response


@view_config(route_name="image_next", renderer='json')
def image_next(request):
    image = request.matchdict['image']
    date = image.split('_')[0]
    event_name = request.matchdict['event']
    images = request.db.view('_design/images/_view/all', reduce=False,
                              start_key=[event_name, date, image],
                              limit=1, skip=1)

    if images.rows:
        return HTTPFound(location=request.route_path('image', event=event_name, image=images.rows[0].id))

    return HTTPFound(location=request.route_path('image', event=event_name, image=image))

@view_config(route_name="image_prev", renderer='json')
def image_prev(request):
    image = request.matchdict['image']
    date = image.split('_')[0]
    event_name = request.matchdict['event']
    images = request.db.view('_design/images/_view/all', reduce=False,
                              start_key=[event_name, date, {}],
                              limit=1, skip=1, descending=True)

    if images.rows:
        return HTTPFound(location=request.route_path('image', event=event_name, image=images.rows[0].id))

    return HTTPFound(location=request.route_path('image', event=event_name, image=image))
