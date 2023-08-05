from threading import Thread
#from dateparser.search import search_dates
from time import sleep
from threading import RLock, Condition, Lock

from .LogLineCollection import LogLineCollection, LogLine

class SourceMonitorThread(Thread):
    '''
    A thread that monitors a log file for new log activity

        +------+       +-------------------------------+
        |     \|       | get_new_chars()               |
        |Source+------->  * Check source for new chars |
        |      |       |  * decode bytes -> chars      |
        +------+       |  * detect file trunc          |
                       +--+----------------------------+
                          |
                          |new chars
                          |
                       +--v----------------------------+
                       | handle_new_chars()            |
                       |  * convert char stream to     |
                       |    lines                      |
                       |  * detect duplicate lines?    |
                       +--+----------------------------+
                          |
                          |new lines
                          |
                       +--v----------------------------+
                       | new_line()                    |
                       |  * Detect Dates               |
                       |  * Add metadata               |
                       +-------------------------------+

    '''

    def __init__(self, monitor_id, name, sleep_sec=1):
        self.__monitor_id = monitor_id
        self.__name = name
        self.__sleep_for = sleep_sec

        self.collection = LogLineCollection()

        #self.monitor_lock = RLock()

        super().__init__(daemon=True, name=name)

        self.__new_char_buffer = ''
        self.__next_line_num = 1


    @property
    def monitor_id(self):
        return self.__monitor_id


    @property
    def source_spec(self):
        '''What to display to the user on what this is monitoring'''
        return self.__name


    def run(self):
        while True:
            new_data = self.get_new_chars()
            if new_data is not None:
                for line in self.handle_new_chars(new_data):
                    self.handle_new_line(line)
            else:
                sleep(self.__sleep_for)


    # -- Log capture methods --

    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: yield new chars (forever)
        '''
        raise NotImplementedError()
        if False:
            yield None


    def handle_new_chars(self, chars):
        '''
        New characters read from monitored log source

        Called repeatedly, and should buffer characters not returned yet.

        Base implementation acts like readline from incoming char stream.

        :param chars: Alread decoded characters
        :return:
            Generate LogLine
            Any new, full lines detected from the character stream (in order)
        '''
        lines = (self.__new_char_buffer + chars).split("\n")
        for line in lines[:-1]:
            if len(line) > 0:
                yield LogLine(
                    txt = line,
                    source_name = self.__name,
                    monitor_id = self.__monitor_id)

        if lines[-1].endswith("\n"):
            yield LogLine(
                txt = lines[-1],
                source_name = self.__name,
                monitor_id = self.__monitor_id)
            self.__new_char_buffer = ''
        else:
            self.__new_char_buffer = lines[-1]



    def handle_new_line(self, line):
        '''
        Handle new line detect from the input

        1) Performs metadata extraction like line number and date string

        :param line: LogLine
        '''

        # Look for timestamp
        # detected = search_dates(line.txt, languages=['en'])
        # if len(detected) > 0:
        #     line.ts = min(detected)

        # TODO: Detect duplicate lines here?

        # Save line
        line.linenum = self.__next_line_num
        self.__next_line_num += 1
        self.collection.add(line)

