from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time
from urllib.parse import urlparse


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.lock = None
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            # add frontier lock
            self.frontier.fLock.acquire()
            tbd_url = self.frontier.get_tbd_url()

            # examin domain lock, set accordingly
            domain = urlparse(tbd_url).netloc

            if ".ics.uci.edu" == domain:
                self.lock = self.frontier.icslock
                self.lock.acquire()
            elif ".cs.uci.edu" == domain:
                self.lock = self.frontier.cslock
                self.lock.acquire()
            elif ".informatics.uci.edu" == domain:
                self.lock = self.frontier.infolock
                self.lock.acquire()
            elif ".stat.uci.edu" == domain:
                self.lock = self.frontier.statlock
                self.lock.acquire()
            elif "today.uci.edu" == domain:
                self.lock = self.frontier.todaylock
                self.lock.acquire()

            # release frontier lock 
            self.frontier.fLock.release()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                # lock F
                self.frontier.fLock.acquire()
                self.frontier.add_url(scraped_url)
                # release F
                self.frontier.fLock.release()
            
            # MIGHT NOT BE NEEDED
            # lock F
            self.frontier.fLock.acquire()
            self.frontier.mark_url_complete(tbd_url)
            # release F
            self.frontier.fLock.release()
            time.sleep(self.config.time_delay)
            # release domain lock
            self.lock.release()
