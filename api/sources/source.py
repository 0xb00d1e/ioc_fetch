class Source:
    def check_ipv4(self, ipv4):
        raise NotImplementedError

    def check_domain(self, domain):
        raise NotImplementedError

    def check_md5(self, md5):
        raise NotImplementedError

    def check_sha1(self, sha1):
        raise NotImplementedError

    def check_sha256(self, sha256):
        raise NotImplementedError
