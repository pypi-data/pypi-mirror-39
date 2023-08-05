'''Collect the log line collection functionality here'''
from threading import Lock, RLock, Condition

class LogLineID:
    '''
    Unique ID for log lines

    Assigned globally (across monitors) and sequentially
    '''

    LOCK = Lock()
    NEXT_ID = 0

    def __init__(self, log_id=None):
        if log_id is None:
            with LogLineID.LOCK:
                self.__id = LogLineID.NEXT_ID
                LogLineID.NEXT_ID += 1
        else:
            self.__id = int(log_id)

    def __repr__(self):
        return "LogLineID(%d)" % (self.__id)
    def __str__(self):
        return str(self.__id)
    def __eq__(self, other):
        try:
            return self.__id == other.__id
        except:
            return False
    def __ne__(self, other):
        return not self == other
    def __lt__(self, other):
        try:
            return self.__id < other.__id
        except:
            try:
                return self.__id < int(other)
            except:
                raise ValueError("Can't compare")
    def __gt__(self, other):
        try:
            return self.__id > other.__id
        except:
            try:
                return self.__id > int(other)
            except:
                raise ValueError("Can't compare")
    @property
    def i(self):
        return self.__id


class LogLine:
    '''Encapsulate a line from a log file'''

    def __init__(self, txt, source_name, monitor_id):
        self.__txt = txt
        self.__source = source_name
        self.linenum = None             # Line number in source file
        self.ts = None                  # Time the line was seen
        self.line_id = LogLineID()      # GUID
        self.monitor_id = monitor_id    # Monitor ID of source

    @property
    def txt(self):
        return self.__txt

    @property
    def source_name(self):
        return self.__source

    def __str__(self):
        return self.txt

    def __repr__(self):
        return "%s:%s %s" % (self.source_name, self.linenum or '-', self.txt)


class NoNewLines(Exception): pass


class LogLineCollection:
    '''Collection of collected log lines'''

    MAX_SIZE = 30 * 1024 * 1024

    def __init__(self):
        self.__lock = RLock()
        self.__new_lines_avail = Condition(lock=self.__lock)
        self.__lines = list()
        self.__size = 0

        self._log_group = None # See LogLineGroup.add_collection()


    def add(self, line):
        '''
        Add a line to the collection

        :param line: LogLine
        '''
        with self.__lock:
            self.__lines.append(line)
            self.__size += len(line.txt)

            # Check size, drop 25% if too many
            if self.__size >= self.MAX_SIZE:
                self.__lines = self.__lines[int(0.25*len(self.__lines)):]
                self.__size = sum([len(l.txt) for l in self.__lines])

            # Notify anyone waiting
            # Note: We need to have the lock to do this, but we already have it
            self.__new_lines_avail.notify_all()
            if self._log_group is not None:
                self._log_group.notify_new_lines()


    # --- Query Methods ---

    def all_lines(self):
        with self.__lock:
            for line in self.__lines:
                yield line


    def last_lines(self, num=None):
        if num is None:
            with self.__lock:
                for i in range(len(self.__lines)-1, 0-1, -1):
                    yield self.__lines[i]
        else:
            for i, line in enumerate(self.last_lines()):
                if i < num:
                    yield line
                else:
                    return


    @property
    def last_line(self):
        with self.__lock:
            if len(self.__lines) > 0:
                return self.__lines[-1]
            else:
                return None


    # --- Waiting for new data ---

    def wait_new_line_available(self, last_line_id, timeout_sec):
        '''
        Hold until either a new line has been detected in the log, or a timeout occurs

        Don't need to hold lock to call this, as it will use the condition to wait until
        available.

        :param last_line_id:
            The last LogLine.line_id the caller knows of.
            Will only return lines greater than this.
        :param timeout_sec:
            The number of seconds to wait before timing out
        :return:
            List of new lines
        :raises NoNewLines:
            If the timeout occurs
        '''

        # Custom condition check function that respects last_line_id
        def _check_new_line_available():
            last = self.last_line
            if last is not None:
                if last_line_id is None or last.line_id > last_line_id:
                    return True
            return False

        # Get condition lock (which gets collection lock)
        with self.__new_lines_avail:

            # Wait for new line to be available
            while not _check_new_line_available():
                # wait() releases lock.  Will return False on timeout
                if not self.__new_lines_avail.wait(timeout=timeout_sec):
                    raise NoNewLines()

            # Lock is req-aquired here and we know there's new data

            # Collect all new lines
            lines = list()
            for line in self.last_lines():
                if last_line_id is None or line.line_id > last_line_id:
                    lines.append(line)
                else:
                    break

        return list(reversed(lines)) # Return oldest new line on top [0]


class LogLineGroup:
    '''
    Group multiple LogLineCollections together

    Used so that we can create a condition on any new lines in the whole group
    '''

    def __init__(self):
        self.__new_lines_avail = Condition()
        self.__members = list()


    def add_collection(self, col):
        '''Add a collection to the group'''
        col._log_group = self
        self.__members.append(col)


    def notify_new_lines(self):
        '''Notify any threads waiting that there is new log data'''
        with self.__new_lines_avail:
            self.__new_lines_avail.notify_all()


    def wait_new_line_available(self, last_line_id, timeout_sec):
        '''
        Hold until either a new line has been detected in the log, or a timeout occurs

        Don't need to hold lock to call this, as it will use the condition to wait until
        available.

        :param last_line_id:
            The last LogLine.line_id the caller knows of.
            Will only return lines greater than this.
            Since Log IDs are global, will return if any monitor
        :param timeout_sec:
            The number of seconds to wait before timing out
        :return:
            List of new lines
        :raises NoNewLines:
            If the timeout occurs
        '''

        # Custom condition check function that respects last_line_id
        def _new_line_available():

            for col in self.__members:
                last = col.last_line
                if last is not None:
                    if last_line_id is None or last.line_id > last_line_id:
                        return True
            return False

        # Get condition lock (which gets collection lock)
        with self.__new_lines_avail:

            # Wait for new line to be available
            while not _new_line_available():
                # wait() releases lock.  Will return False on timeout
                if not self.__new_lines_avail.wait(timeout=timeout_sec):
                    raise NoNewLines()

            # Lock is req-aquired here and we know there's new data

            # Collect all new lines (from all collections in this group)
            lines = list()
            for col in self.__members:
                for line in col.last_lines():
                    if last_line_id is None or line.line_id > last_line_id:
                        lines.append(line)
                    else:
                        break # last_lines is a generator, so this is pretty efficient

        # Return oldest new line on top [0]
        return list(sorted(lines, key=lambda line: line.line_id))