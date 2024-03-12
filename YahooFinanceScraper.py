import Runtime_Data
import random
import time

class YFScraper:
    def __init__(self):
        self.runtime_Data = Runtime_Data()
        return
    
    def sleep(self, minSeconds, maxSeconds):
        sleep_time = random.uniform(minSeconds, maxSeconds)
        self.runtime_Data.sleep_duration += sleep_time
        time.sleep(sleep_time)
        return

    
    def scrape(self):
        self.runtime_Data.start()


        self.runtime_Data.end()
        return