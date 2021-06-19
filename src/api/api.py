import requests
import json
from types import SimpleNamespace
from threading import Lock
import traceback
from . import keyring
from datetime import date
import threading

#Keys from project twitter-crawler and app twitter-crawler
#NMr3bgW5x0GYZoPXCXg2Bp96IA1u3OaRjp7F7QpiiRTxOm6X6T API Key
#1aktqLyBodVz4KK9BvpuYdVAz API Secret key
#AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k Bearer Token

# General API Exception. Any API exception can be caught from it.
class ApiError(Exception):
    
    def __init__(self, message="Twitter API returned error code {}", code=000):
        if code != 000:
            self.message = message.format(code)
        else:
            self.message = message
        super().__init__(self.message)

# Rate Limit API exception code 429
class RateLimitError(ApiError):

    def __init__(self, message="Rate limit have been exhausted for the resource."):
        super().__init__(message=message)

# Forbidden API exception code 403
class ForbiddenError(ApiError):

    def __init__(self, message="Request was actively refused by API."):
        super().__init__(message=message)

# Not Found API exception code 404
class NotFoundError(ApiError):

    def __init__(self, message="Endpoint was not found."):
        super().__init__(message=message)

# Exception handler
def raiseError(code):
    if code == 429:
        raise RateLimitError()
    if code == 403:
        raise ForbiddenError()
    if code == 404:
        raise NotFoundError()
    raise ApiError(code=code)

# Manage get requests to Twitter API. It expects App authenticaton
# only.

class Api():

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Api, cls).__new__(cls)
            return cls._instance

    # Setup default parameters that request should return.

    def __init__(self):
        self.tweets = "id,text,created_at,author_id,public_metrics,entities"
        self.users = "id,username,description,public_metrics,verified,created_at"
        self.expansions = "referenced_tweets.id,author_id,entities.mentions.username,referenced_tweets.id.author_id"
        self.keys_user_timeline = keyring.Keyring()

    # Set the bearer token at the header of request. The bearer token 
    # allows more calls than the standart one.

    def auth(self, bearer_token):
        return {"Authorization": "Bearer {}".format(bearer_token)}

    # Perform the GET request to Twitter API, deserializing the JSON
    # response into a python object Status.

    def call(self, url, key, params):
        response = requests.request("GET", url, headers=self.auth(key), params=params) # GET request to URL endpoint
        if response.status_code != 200:
            raiseError(response.status_code)
        return json.loads(json.dumps(response.json()), object_hook=lambda d: SimpleNamespace(**d)) # Turns raw json into python object.

    # Handle status pagination. It yields statuses until there're no more
    # left or the limit stablished of pages was reached.

    def paginator(self, npages, keyring, url, key, parameters):
        page = 0
        stop = False
        while not stop:
            page += 1
            status = self.call(url, key, parameters)
            if hasattr(status.meta, "next_token") and page < npages:                   
                parameters["pagination_token"] = status.meta.next_token
            else:
                stop = True
            yield status

    def limit_handler(self, paginator, key, keyring):
        while True:
            try:
                yield next(paginator)
            except RateLimitError:
                print(str(threading.get_ident()) + "Key exhausted")
                key = keyring.request()
                continue
            except ForbiddenError:
                continue
            except ApiError as e:
                with open('log-twitter-api.txt', 'a+') as log:
                    log.write(str(date.today()) + ": Twitter API reported an error: " + str(e) + " \n")
                    log.write(traceback.format_exc())
                break
            except StopIteration:
                keyring.return_key(key)
                break

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
        key = self.keys_user_timeline.request()
        return self.limit_handler(self.paginator(npages, self.keys_user_timeline, url, key, parameters), key, self.keys_user_timeline)

    # TODO: Full-archive historical search. ALWAYS USE 'paginator' function!
    # TODO: Recent search. ALWAYS USE 'paginator' function!

