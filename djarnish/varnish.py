# -*- coding: utf-8 -*-
from http import client

from django.conf import settings


class DjarnishPurgeException(Exception):
    pass


def purge(url):
    for varnish_server in getattr(settings, "DJARNISH_SERVERS", []):
        conn = client.HTTPConnection(varnish_server)
        conn.request("PURGE", url)
        response = conn.getresponse()
        if response.status != 200:
            raise DjarnishPurgeException(response.status, str(response.msg))
