from collections import namedtuple

ConfigurationFetchResult = namedtuple('ConfigurationFetchResult', ['data', 'source'])


class ConfigurationSource:
    CDN = 'CDN'
    API = 'API'
    ROXY = 'Roxy'
