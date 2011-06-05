from django.core.management.base import BaseCommand, CommandError
from hashed_url.utilities import get_hashed_url

class Command(BaseCommand):
    args = '<absolute_url ...>'
    help = 'Provides a valid hashed URL (several URLs may be specified)'

    def handle(self, *args, **options):
        for url in args:
            print get_hashed_url(url)
