import requests

from ioc_fetch.api.sources.source import Source
from ioc_fetch.lib.util import get_env_variable


class Shodan(Source):
    def __init__(self):
        self.url = 'https://api.shodan.io'
        self.api_key = get_env_variable('SHODAN_API_KEY')

    def check_ipv4(self, ipv4):
        response = requests.get(
            f'{self.url}/shodan/host/{ipv4}?key={self.api_key}'
        )
        return response
