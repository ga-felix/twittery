from api import api
from db.sql import sql
#AAAAAAAAAAAAAAAAAAAAAJuREwEAAAAAukvvr2OOF2qlClD%2BghDAGn%2FfiFQ%3D3JdR1mASBmL00tGRaim0rk7c08knREM2D59Xa5Xb5z2qQuRVQg
def foo():
    a = api.Api()
    db = sql.Sql("twitter", "root", "zxc12989")
    a.auth("AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k")
    result = a.user_timeline(128372940)
    print(str(result))
    print(str(result.data))
    #for r in result:
        #print("Resposta: " + str(r) + "#########\n")
        #db.insertTweet(r)
        #db.insertAccount(r["include"].users)
        #for t in r.referenced_tweets.id:
            #db.insertTweet(t)
            #print("Referenciado: " + t.text)

if __name__ == "__main__":
    foo()