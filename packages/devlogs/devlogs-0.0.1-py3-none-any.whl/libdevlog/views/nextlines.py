import json
from ..monitors import NoNewLines

TIMEOUT_SEC=15.0

def nextlines_view(request, server, assets):
    '''
    Wait for new lines to be detected

    Note: run with auto-lock disabled.  This view will aquire lock as needed.
    This allows it to not hold the lock while waioting for new data

    Expected GET parameters (in GET body I believe):
        monitor_id      = The monitor to get log lines from or "all"
        last_line_id    = The last line ID the caller knows of (-1: None)
        how_many        = "1" or "all"

    '''

    # Request parameters
    if request["monitor_id"] == "all":
        monitor_id = None
    else:
        monitor_id = int(request['monitor_id'])

    last_line_id = int(request['last_line_id'])
    if last_line_id == -1:
        last_line_id = None

    multiple = request['how_many'] == "all"

    # Determine which object we want to query for new data
    with server.lock:
        if monitor_id is None:
            watch = server.all_log_lines
        else:
            try:
                watch = server.monitors[monitor_id].collection
            except Exception as e:
                return json.dumps({
                    'status': 'error',
                    'msg': "Invalid monitor ID: " + str(e)
                })

    # Request next line
    try:
        new_lines = watch.wait_new_line_available(last_line_id, TIMEOUT_SEC)
    except NoNewLines:
        new_lines = None

    # Return no data
    if new_lines is None:
        return json.dumps({
            'status': 'nodata',
            'msg': 'no new data',
        })

    # Encapsulate response
    if not multiple:
        new_lines = new_lines[-1:]

    return json.dumps({
        'status': 'ok',
        'cnt': len(new_lines),
        'lines': [
            {
                'text': line.txt,
                'line_id': line.line_id.i,
                'monitor_id': line.monitor_id,
            } for line in new_lines
        ]
    })

