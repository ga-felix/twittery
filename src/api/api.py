import requests
import json
from . import error
from types import SimpleNamespace

#Keys from project twitter-crawler and app twitter-crawler
#NMr3bgW5x0GYZoPXCXg2Bp96IA1u3OaRjp7F7QpiiRTxOm6X6T API Key
#1aktqLyBodVz4KK9BvpuYdVAz API Secret key
#AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k Bearer Token

# Manage get requests to Twitter API. It expects App authenticaton
# only.

class Api():

    # Setup default parameters that request should return.

    def __init__(self):
        self.tweets = "id,text,created_at,author_id,public_metrics,entities"
        self.users = "id,username,description,public_metrics,verified,created_at"
        self.expansions = "referenced_tweets.id,author_id,entities.mentions.username,referenced_tweets.id.author_id"

    # Set the bearer token at the header of request. The bearer token 
    # allows more calls than the standart one.

    def auth(self, bearer_token):
        self.bearer_token = bearer_token
        self.header = {"Authorization": "Bearer {}".format(self.bearer_token)}

    # Perform the GET request to Twitter API, deserializing the JSON
    # response into a python object Status.

    def call(self, url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params) # GET request to URL endpoint
        if response.status_code != 200:
            error.raiseError(response.status_code)
        return json.loads(json.dumps(response.json()), object_hook=lambda d: SimpleNamespace(**d)) # Turns raw json into python object.

    # Handle status pagination. It yields statuses until there're no more
    # left or the limit stablished of pages was reached.

    def paginator(self, npages, request, *args):
        page = 0
        while True:
            if page == npages:  # Page limit was reached? If true
                break           # then leave.
            page += 1
            try:
                status = request(*args)
            except error.ApiError as e: # TODO: if a generator raises Exception, is it possible to consume it from the point
                raise e                 # before Exception was raised? This could possibly save not necessary API calls
            if not hasattr(status.meta, "next_token"): # Is still possible to paginate? If not
                break                                  # then leave.
            args[2]["pagination_token"] = status.meta.next_token
            yield status

    # Request to User Timeline endpoint. Check Twitter API documentation
    # for further details.

    def user_timeline(self, id, npages=-1, max_results=10, start_time=None, end_time=None):
        parameters = dict()
        parameters['tweet.fields'] = self.tweets
        parameters['user.fields'] = self.users
        parameters['expansions'] = self.expansions
        parameters['max_results'] = max_results
        if start_time:
            parameters['start_time'] = start_time
        if end_time:
            parameters['end_time'] = end_time
        url = 'https://api.twitter.com/2/users/{}/tweets'.format(id)
        return self.paginator(npages, self.call, url, self.header, parameters)

    # TODO: Full-archive historical search. ALWAYS USE 'paginator' function!
    # TODO: Recent search. ALWAYS USE 'paginator' function!