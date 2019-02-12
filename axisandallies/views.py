from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/aaa.jinja2')
def my_view(request):
    if request.method == 'GET':
        pass
    return {'project': 'AxisAndAllies'}
