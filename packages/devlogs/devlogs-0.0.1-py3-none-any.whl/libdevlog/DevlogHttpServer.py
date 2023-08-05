import os

from devhttp import DevelopmentHttpServer

from . import views

from .monitors import LogTailMonitor
from .monitors import LogLineGroup

class DevlogHttpServer(DevelopmentHttpServer):
    '''
    Web app server for showing monitored log content
    '''

    def __init__(self, config, project_folder=None):
        '''

        :param config:
            DevlogConfig config file for server

        :param project_folder:
            Path to project folder for locating assets

            If project_folder is specified, then find and load assets from project
            folder files.
            If not speicified, then will load assets saved to module devlogs.assets
        '''

        super().__init__()

        # Load assets (statics and templates)
        if project_folder is None:
            from .DevlogHttpAssets import STATIC_DATA
            self.load_assets_module(STATIC_DATA)
        else:
            self._add_file_assets(project_folder)

        self._configure()

        self.config = config
        self.monitors = list()
        self.all_log_lines = LogLineGroup()

        self.add_monitors_from_config()


    def _configure(self):

        # Dynamic views
        self.add_dynamic('index.html', views.index_view)
        self.add_dynamic('log.html', views.log_view)

        self.add_dynamic('status', views.status_view, content_type='application/json')
        self.add_dynamic('nextlines', views.nextlines_view, content_type='application/json', autolock=False)

        # Redirects
        self.redirect('', 'index.html')


    def _add_file_assets(self, project_folder):
        '''
        Add all of the assets this server needs from disk

        :param project_folder:
            Path to the project folder for locating assets
        '''
        assets = os.path.join(project_folder, 'assets')
    
        for bootstrap_dir in ('css', 'js', 'vendor'):
            self.add_multiple_static(
                bootstrap_dir,
                os.path.join(project_folder, 'lib', 'startbootstrap-sb-admin', bootstrap_dir))

        # Static Assets
        self.add_static('favicon.ico', os.path.join(assets, 'favicon.ico'))
        self.add_static('css/devlogs.css', os.path.join(assets, 'css', 'devlogs.css'))

        # Templates
        self.add_asset('base.j2.html', os.path.join(assets, 'base.j2.html'))
        self.add_asset('index.j2.html', os.path.join(assets, 'index.j2.html'))
        self.add_asset('log.j2.html', os.path.join(assets, 'log.j2.html'))

        # JS Assets
        self.add_static('js/status-check.js', os.path.join(assets, 'js', 'status-check.js'))
        self.add_static('js/lastline-update.js', os.path.join(assets, 'js', 'lastline-update.js'))
        self.add_static('js/log-tail.js', os.path.join(assets, 'js', 'log-tail.js'))

        # jquery-ui files
        lib = os.path.join(project_folder, 'lib', 'jquery-ui-1.12.1')
        for filename in ('jquery-ui.js', 'jquery-ui.css'):
            path = os.path.join(lib, filename)
            if not os.path.exists(path):
                raise Exception("Missing asset: " + path)
            self.add_static('jquery-ui/'+filename, path)


    def add_monitors_from_config(self):
        '''
        Craete monitor workers/threads for each entry listed in config
        '''
        for monitor_config in self.config.monitors:
            monitor_id = len(self.monitors)
            if monitor_config.monitor_type == 'tail':

                monitor = LogTailMonitor(
                    path = monitor_config.path,
                    monitor_id = monitor_id)

                self.monitors.append(monitor)

                self.all_log_lines.add_collection(monitor.collection)


    def start_monitors(self):
        '''
        Start all of the monitor threads
        '''
        for monitor in self.monitors:
            monitor.start()






