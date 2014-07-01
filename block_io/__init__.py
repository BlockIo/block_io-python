import requests

VERSION="0.1.3"

class BlockIo(object):

    def __init__(self, api_key):
        # initiate the object
        self.api_key = api_key
        self.base_url = 'https://block.io/api/v1/API_CALL/'

    def __getattr__(self, attr, *args, **kwargs):
        
        def hook(*args, **kwargs):
            return self.api_call(attr, **kwargs)
        return hook

    def api_call(self, method, **kwargs):
        # the actual API call
        
        # http parameters
        payload = {}

        if self.api_key is not None:
            payload["api_key"] = self.api_key
            
        payload.update(kwargs)

        # update the parameters with the API key
        response = requests.get(self.base_url.replace('API_CALL',method), params = payload)

        return response.json()

