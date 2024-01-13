import requests
import json


class APICall:

    def __init__(self, url):
        self.url = url

    def fetch_data(self, startTimestamp, endTimestamp):
        payload = {
            'startTimestamp': startTimestamp,
            'endTimestamp': endTimestamp
        }
        response = requests.post(self.url, data=payload)
        data = response.json()
        return data
