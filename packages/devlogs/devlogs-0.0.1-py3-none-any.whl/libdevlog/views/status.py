import json

def status_view(request, server, assets):
    '''Simple response to show server is up'''
    return json.dumps({'status': 'ok'})

