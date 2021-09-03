from database.sql import sql
from extractor import extractor
from settings import settings
from reporter import reporter
import threading
import pandas as pd

def main():
    #thread1 = threading.Thread(target = extractor.download_recent_tweets, args = ("#Bolsonaro2022",),
        #kwargs={'npages': 1}, name='download_recent_tweets')
    #thread2 = threading.Thread(target = extractor.download_user_timeline, args = (),
        #kwargs={'npages': -1}, name='download_user_timeline')
    #thread3 = threading.Thread(target = extractor.download_historical_tweets, args = ("(Unesco OR PIB) lang:pt is:retweet",),
        #kwargs={'npages': 10, 'start_time': '2013-01-01T00:00:00Z', 'end_time': '2013-12-31T23:59:59Z'})
    #thread4 = threading.Thread(target = reporter.create_graph, args = ("retweets",))
    #thread1.start()
    #thread2.start()
    #thread3.start()
    #thread4.start()
    df = pd.read_csv("settings/targets/medias-profiles.csv")
    for user in df['Conta']:
        extractor.download_historical_tweets("(Unesco OR PIB) lang:pt is:retweet retweets_of:" + user,
                                            start_time = '2012-07-01T00:00:00Z', end_time = '2012-07-01T23:59:59Z')
    
if __name__ == "__main__":
    settings.init()
    main()