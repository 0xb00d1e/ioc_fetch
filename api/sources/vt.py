import requests

from ioc_fetch.api.sources.source import Source
from ioc_fetch.lib.util import get_env_variable


class VT(Source):
    def __init__(self):
        self.url = 'https://www.virustotal.com/api/v3'
        self.api_key = get_env_variable('VT_API_KEY')

    def check_ipv4(self, ipv4):
        response = requests.get(
            f'{self.url}/ip_addresses/{ipv4}',
            headers={'x-apikey': self.api_key}
        )
        return response

    def check_domain(self, domain):
        response = requests.get(
            f'{self.url}/domains/{domain}',
            headers={'x-apikey': self.api_key}
        )
        return response

    def check_md5(self, md5):
        response = requests.get(
            f'{self.url}/files/{md5}',
            headers={'x-apikey': self.api_key}
        )
        return response

    def check_sha1(self, sha1):
        response = requests.get(
            f'{self.url}/files/{sha1}',
            headers={'x-apikey': self.api_key}
        )
        return response

    def check_sha256(self, sha256):
        response = requests.get(
            f'{self.url}/files/{sha256}',
            headers={'x-apikey': self.api_key}
        )
        return response
