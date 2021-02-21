from ioc_fetch.api.sources import shodan
from ioc_fetch.api.sources import vt


all_sources = [
    shodan.Shodan(),
    vt.VT()
]
