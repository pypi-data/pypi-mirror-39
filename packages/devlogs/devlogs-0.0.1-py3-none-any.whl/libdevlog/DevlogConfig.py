import os
from textwrap import dedent
import yaml


class ConfigFileSyntaxError(Exception): pass


class DevlogConfigSection:
    '''A section of the config file'''
    def __init__(self, path, info, entry_name=None):
        self.__path = path
        self.__name = entry_name
        self.info = info
    def _syntax_error(self, msg):
        if self.__name is None:
            raise ConfigFileSyntaxError("Error in %s: %s" % (self.__path, msg))
        else:
            raise ConfigFileSyntaxError("Error in %s record in %s: %s" % (
                self.__name, self.__path, msg))
    @property
    def entry_name(self):
        return self.__name


class DevlogLogConfig(DevlogConfigSection):
    '''Entry in logs: in config file'''

    @property
    def path(self):
        '''Path to monitor'''
        try:
            return self.info['path']
        except KeyError:
            self._syntax_error("Missing required path")

    @property
    def monitor_type(self):
        try:
            return self.info['type']
        except KeyError:
            return 'tail'


class DevlogConfig:
    '''Config file for server'''

    TEMPLATE = dedent("""\
        ---
        logs:
         - path: /var/log/syslog
         - cmd:  systemctl status ssh
           type: command
        commands:
         - name:     Build
           title:    Build Test Server
           working:  /vagrant/devlog
           commands:
            - title: Run tests
              cmd:   run_tests.sh
            - title: Collect Statics
              cmd:   python manage.py collectstatic
        """)


    def __init__(self, path):
        '''Config file directs devlog server on what to present'''

        if not os.path.exists(path):
            raise KeyError("%s does not exist" % (self.__path))

        self.__data = None
        self.__path = path

        self._load(path)


    def _load(self, path):
        with open(path, 'r') as fh:
            self.__data = yaml.load(fh)


    def _syntax_error(self, msg):
        raise ConfigFileSyntaxError("Error in %s: %s" % (self.__path, msg))

    @property
    def monitors(self):
        '''
        List the monitored log files

        :return: DevlogLogConfigs
        '''
        try:
            for info in self.__data['logs']:
                yield DevlogLogConfig(self.__path, info)

        except KeyError:
            self._syntax_error("Missing logs: section")


class NullDevlogConfig(DevlogConfig):

    def __init__(self):
        self.__data = dict()

    @property
    def monitors(self):
        if False:
            yield None
