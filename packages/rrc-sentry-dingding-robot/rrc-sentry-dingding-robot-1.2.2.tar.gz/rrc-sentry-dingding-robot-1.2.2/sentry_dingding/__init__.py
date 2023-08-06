# encoding=utf-8

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('rrc-sentry-dingding-robot').version
except Exception, e:
    VERSION = '1.2.2'
