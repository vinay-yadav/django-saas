from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'localhost', settings.ROOT_URLCONF, name='localhost'),
    host(r'^desalsa', settings.ROOT_URLCONF, name='desalsa'),
    host(r'^invalid', settings.ROOT_URLCONF, name='invalid'),
    host(r'(?P<subdomain>[\w.@+-]+)', settings.ENT_URLCONF, name='enterprises'),
)