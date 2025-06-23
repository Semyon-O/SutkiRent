import datetime
import time
from pprint import pprint

from django.core.management.base import BaseCommand

from objects.services import realtycalendar
from objects.models import *
RC = realtycalendar.viewmodels.RealtyCalendar("https://realtycalendar.ru/v2/widget/AAAwUw")


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        objects = Object.objects.all()
        print(len(objects))
        for obj in objects:
            today = datetime.date.today()
            cur_year = today.year
            cur_month = today.month
            cur_day = today.day
            object_dates = RC.get_object_date(obj.pk,
                                              begin_date=f"{cur_year}-{cur_month}-{cur_day}",
                                              end_date=f"{cur_year+1}-1-01")
            print(f"FOR OBJECT [{obj.pk}] ({cur_year}-{cur_month}-{cur_day} - {cur_year+1}-1-01) THIS DATES")
            pprint(object_dates)
            for obj_date in object_dates:
                DailyPrice.objects.update_or_create(
                    object=obj,
                    date=obj_date.date,
                    price=obj_date.price,
                    is_available=obj_date.available,
                    min_stay_days=obj_date.min_stay,
                )
            print("DONE")
