from devhttp import render_jinja

def index_view(request, server, assets):
    return render_jinja(assets, 'index.j2.html', server=server)

