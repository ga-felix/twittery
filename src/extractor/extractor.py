from api import api
from settings import settings
from database.sql import sql
import time

#def download_user_timeline():

def foo():
    a = api.Api()
    db = sql.Sql("twitter", "root", "zxc12989")
    count = 0

    for user in settings.user_timeline:
        pages = a.user_timeline(user, npages=2, max_results=5)
        for page in pages:
            count += 1
            #for result in page.data:
                #print(result.id)
            time.sleep(0.1)

if __name__ == "__main__":
    foo()