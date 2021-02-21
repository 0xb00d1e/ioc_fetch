from ioc_fetch.api.sources import abuse_ip_db
from ioc_fetch.api.sources import shodan
from ioc_fetch.api.sources import vt


all_sources = [
    abuse_ip_db.AbuseIPDB(),
    shodan.Shodan(),
    vt.VT()
]
