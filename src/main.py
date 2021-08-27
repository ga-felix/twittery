from database.sql import sql
from extractor import extractor
from settings import settings
from reporter import reporter
import threading

def main():
    #thread1 = threading.Thread(target = extractor.download_recent_tweets, args = ("#Bolsonaro2022",),
        #kwargs={'npages': 1}, name='download_recent_tweets')
    #thread2 = threading.Thread(target = extractor.download_user_timeline, args = (),
        #kwargs={'npages': -1}, name='download_user_timeline')
    #thread3 = threading.Thread(target = extractor.download_historical_tweets, args = ("#ForaDilma",),
        #kwargs={'npages': 1, 'start_time': '2013-01-01T00:00:00Z', 'end_time': '2013-12-31T23:59:59Z'})
    #thread4 = threading.Thread(target = reporter.create_graph, args = ("retweets",))
    #thread1.start()
    #thread2.start()
    #thread3.start()
    #thread4.start()
    extractor.download_retweeters(1431027344530198528)
    
if __name__ == "__main__":
    settings.init()
    main()