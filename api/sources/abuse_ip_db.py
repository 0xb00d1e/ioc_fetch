import requests

from ioc_fetch.api.sources.source import Source
from ioc_fetch.lib.util import get_env_variable


class AbuseIPDB(Source):
    def __init__(self):
        self.url = 'https://api.abuseipdb.com/api/v2/check'
        self.api_key = get_env_variable('ABUSE_IP_DB_API_KEY')

    def check_ipv4(self, ipv4):
        response = requests.get(
            f'{self.url}',
            headers={
                'Accept': 'application/json',
                'Key': self.api_key
            },
            params={
               'ipAddress': ipv4
            }
        )
        return response
