# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from ...varnish import purge


class Command(BaseCommand):
    help = _("Purge a url form varnish")

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("url", nargs="+", type=str)

    def handle(self, *args, **options):
        for url in options["url"]:
            purge(url)
