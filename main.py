from app.routes import *
from time import sleep
import threading


class RunScraperHourly(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1

    def run(self):
        while True:
            sleep(20)
            print('Starting scraper')
            get_best_values()
            print('Scraper finished. Running again in one hour.')
            sleep(3600)


scraper_run = RunScraperHourly()


if __name__ == "__main__":
    scraper_run.start()
    app.run(host='0.0.0.0', debug=True)
