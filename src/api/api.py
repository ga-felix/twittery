import requests
import json
from . import exceptions

#Keys from project twitter-crawler and app twitter-crawler
#NMr3bgW5x0GYZoPXCXg2Bp96IA1u3OaRjp7F7QpiiRTxOm6X6T API Key
#1aktqLyBodVz4KK9BvpuYdVAz API Secret key
#AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k Bearer Token

# Data class. It should have no functions, attributes and so on.

class Status(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

# Manage get requests to Twitter API. It expects App authenticaton
# only.

class Api():

    # Select which fields will be returned. It must be concise with the
    # database implementation. 

    def __init__(self):
        self.parameters = {"tweet.fields": "id,text,created_at,author_id,public_metrics", "expansions": "referenced_tweets.id,author_id",
                            "user.fields": "id,username,description,public_metrics,verified,created_at"}

    # Set the bearer token at the header of request. The bearer token 
    # allows more calls than the standart one.

    def auth(self, bearer_token):
        self.bearer_token = bearer_token
        self.header = {"Authorization": "Bearer {}".format(self.bearer_token)}

    # Perform the GET request to Twitter API, deserializing the JSON
    # response into a python object Status.

    def call(self, url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            if response.status_code == 429:
                raise exceptions.RateLimit()
            if response.status_code == 403:
                raise exceptions.Forbidden()
            if response.status_code == 404:
                raise exceptions.NotFound()
            raise exceptions.ApiException("Twitter API error: {} {}".format(response.status_code, response.text))
        return Status(json.dumps(response.json()))

    # Request to User Timeline endpoint. Check Twitter API documentation
    # for further details.

    def user_timeline(self, id):
        url = "https://api.twitter.com/2/users/{}/tweets".format(id)
        status = self.call(url, self.header, self.parameters)
        return status