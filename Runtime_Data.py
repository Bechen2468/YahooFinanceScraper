import time


class Runtime_Data:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.pause_time = None
        self.duration = 0
        self.pause_duration = 0
        self.sleep_duration = 0
        self.scrape_duration = 0

    def start(self):
        self.start_time = time.time()
        self.end_time = None
        self.pause_time = None
        self.duration = 0
        self.pause_duration = 0
        self.sleep_duration = 0
        self.scrape_duration = 0

    def pause(self):
        if self.pause_time is not None:
            return
        self.pause_time = time.time()

    def unpause(self):
        if self.pause_time is None:
            return
        self.pause_duration += time.time() - self.pause_time
        self.pause_time = None

    
    def end(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time - self.pause_duration
