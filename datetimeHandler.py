import datetime
import threading

class datetimeHandler(threading.Thread):
    def __init__(self):
        self.stored = datetime.datetime.now()

    def __run__(self):
        while (1):
            self.stored = datetime.datetime.now()
            