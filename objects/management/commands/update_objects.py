from django.core.management.base import BaseCommand
from objects.services.objects import import_objects_from_rc


class Command(BaseCommand):
    help = 'Download objects info from realtycalendar'

    def handle(self, *args, **options):
        import_objects_from_rc()