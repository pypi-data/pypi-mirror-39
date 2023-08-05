from devhttp import render_jinja

def log_view(request, server, assets):

    # TODO: Implement monitor slug

    monitor_id = int(request['monitor_id'])
    monitor = server.monitors[monitor_id]

    return render_jinja(assets, 'log.j2.html',
        server=server,
        monitor=monitor)

