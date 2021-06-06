from api import api
#AAAAAAAAAAAAAAAAAAAAAJuREwEAAAAAukvvr2OOF2qlClD%2BghDAGn%2FfiFQ%3D3JdR1mASBmL00tGRaim0rk7c08knREM2D59Xa5Xb5z2qQuRVQg
def foo():
    a = api.Api()
    a.auth("AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k")
    a.user_timeline(128372940)

if __name__ == "__main__":
    foo()