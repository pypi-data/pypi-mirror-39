import os
import logging

from .SourceMonitorThread import SourceMonitorThread


class LogTailMonitor(SourceMonitorThread):
    '''Monitor a traditional log file by watching it for new lines'''

    MAX_BYTES = 1024 * 1024

    def __init__(self, path, monitor_id, sleep_sec=1, encoding='utf8'):

        self.__log = logging.getLogger(__name__)

        self.__path = os.path.abspath(path)
        self.__encoding = encoding
        self.__name = "monitor-%s" % (monitor_id)

        if self.__path is not None:
            if os.path.exists(self.__path) and os.path.isfile(self.__path):
                self.__name += '-'+os.path.basename(self.__path)
            else:
                self.__log.warning("%s is not a file or does not exist" % (self.__path))

        super().__init__(monitor_id=monitor_id, name=self.__name, sleep_sec=sleep_sec)

        self.__last_bytes = None
        self.__last_pos = None


    @property
    def source_spec(self):
        '''What to display to the user on what this is monitoring'''
        return self.__path


    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: yield new chars (forever)
        '''

        if os.path.exists(self.__path):

            # Check to see if file shrunk
            if self.__last_pos is not None:
                if os.path.getsize(self.__path) < self.__last_pos:
                    self.__last_pos = None
                    self.__last_bytes = None

            # If last bytes present, see if they're still there
            if self.__last_bytes is not None and self.__last_pos is not None:
                with open(self.__path, 'rt') as fh:
                    last_read_pos = self.__last_pos - len(self.__last_bytes)
                    fh.seek(last_read_pos)
                    if fh.read(len(self.__last_bytes)) != self.__last_bytes:
                        self.__last_pos = None
                        self.__last_bytes = None

            # Determine where to start
            if self.__last_bytes is None or self.__last_pos is None:
                pos = 0
            else:
                pos = self.__last_pos

            # Read new bytes
            with open(self.__path, 'rt') as fh:
                if pos != 0:
                    fh.seek(pos)
                new_data = fh.read(self.MAX_BYTES)

            if not new_data:
                return None

            # Save state for next call
            self.__last_pos = pos + len(new_data)
            self.__last_bytes = new_data

            # # Decode and return (optionally stripping up to 3 chars off tail to help decode)
            # first_decode_e = None
            # for i in (0, 1, 2, 3):
            #     if i > 0:
            #         self.__last_pos -= 1
            #         self.__last_bytes = self.__last_bytes[:-1]
            #     if len(self.__last_bytes) > 0:
            #         try:
            #             return new_data.decode(self.__encoding)
            #         except Exception as e:
            #             if first_decode_e is None:
            #                 first_decode_e = e
            #
            # if first_decode_e:
            #     raise first_decode_e
            # else:
            #     raise Exception("Can we get to here?")

            return new_data





