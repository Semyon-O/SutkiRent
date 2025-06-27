from django.core.management.base import BaseCommand
from objects.services.objects import load_daily_price_per_object


class Command(BaseCommand):
    help = 'Import all daily price from current day to first day of new year'

    def handle(self, *args, **options):
        load_daily_price_per_object()
