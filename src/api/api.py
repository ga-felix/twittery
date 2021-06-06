import requests
import json

#Keys from project twitter-crawler and app twitter-crawler
#NMr3bgW5x0GYZoPXCXg2Bp96IA1u3OaRjp7F7QpiiRTxOm6X6T API Key
#1aktqLyBodVz4KK9BvpuYdVAz API Secret key
#AAAAAAAAAAAAAAAAAAAAAEuQQQEAAAAA4%2FAoRExzxCIxCwgIepWeYC5l6%2BE%3Dz1FPz9VF1U1P9akF4bxSEryEzoiy6EFrgAUNGLsCDVMoY4TM5k Bearer Token

class Api():

    def auth(self, bearer_token):
        self.bearer_token = bearer_token
        self.header = {"Authorization": "Bearer {}".format(self.bearer_token)}

    def call(self, url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
        return response.json()

    def create_parameters(self, parameters):
        line = str()
        for index in range(len(parameters) - 1):
            line += parameters[index] + ","
        line += parameters[len(parameters) - 1]
        return {"tweet.fields": line}

    def user_timeline(self, id):
        paremeters = self.create_parameters(["id", "text", "created_at", "author_id", "public_metrics"])
        url = "https://api.twitter.com/2/users/{}/tweets".format(id)
        json_response = self.call(url, self.header, paremeters)
        print(json.dumps(json_response, indent=4, sort_keys=True))