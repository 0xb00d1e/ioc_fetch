import requests

from ioc_fetch.api.sources.source import Source
from ioc_fetch.lib.util import get_env_variable


class APIVoid(Source):
    def __init__(self):
        self.url = 'https://endpoint.apivoid.com/iprep/v1/pay-as-you-go'
        self.api_key = get_env_variable('APIVOID_API_KEY')

    def check_ipv4(self, ipv4):
        response = requests.get(
            f'{self.url}/?key={self.api_key}&ip={ipv4}'
        )
        return response
