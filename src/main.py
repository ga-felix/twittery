from database.sql import sql
from extractor import extractor
from settings import settings
from reporter import reporter
import threading

def main():
    thread1 = threading.Thread(target = extractor.download_recent_tweets, args = ("#Bolsonaro2022",),
        kwargs={'npages': 1}, name='download_recent_tweets')
    thread2 = threading.Thread(target = extractor.download_user_timeline, args = (),
        kwargs={'npages': -1}, name='download_user_timeline')
    #thread3 = threading.Thread(target = reporter.create_graph, args = ("retweets",))
    #thread3 = threading.Thread(target = extractor.foo, args = ())
    #thread4 = threading.Thread(target = extractor.foo, args = ())
    thread1.start()
    thread2.start()
    #thread3.start()
    #thread4.start()
    
if __name__ == "__main__":
    settings.init()
    main()