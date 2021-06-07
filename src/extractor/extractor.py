from api import api
from settings import settings
from database.sql import sql
import time

#def download_user_timeline():

def foo():
    a = api.Api()
    db = sql.Sql("twitter", "root", "zxc12989")
    a.auth("AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k")
    count = set()
    for user in settings.user_timeline:
        pages = a.user_timeline(user, npages=1, max_results=10)
        for page in pages:
            for result in page.data:
                count.add(result.id)
                print(result.id)
                time.sleep(0.5)
    print("{} tweets coletados ".format(len(count)))

if __name__ == "__main__":
    foo()