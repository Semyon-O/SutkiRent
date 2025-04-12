import logging
import pprint

import requests
from . import models


class RealtyCalendar:

    def __init__(self, url):
        self.url = url

    def get_all_objects(self):
        path_url = "/apartments"
        logging.info(self.url+path_url)
        list_object: list[models.Apartment] = []
        page = 1
        while True:
            response = requests.post(
                self.url + path_url,
                json={
                    "begin_date": None,
                    "end_date": None,
                    "guests": {
                        "adults": 1,
                        "children": []
                    },
                    "apartment_ids": [],
                    "page": page
                }
            )

            if response.status_code == 404:
                return ConnectionError("Not founded resources")

            if response.status_code in (500, 501, 505):
                return ConnectionError("Error with realtycalendar. Check access")

            raw_data = response.json().get("apartments")
            if raw_data in (None, []):
                break

            for raw_object in raw_data:
                serialized_object = models.Apartment(**raw_object)
                list_object.append(serialized_object)

            page += 1
        return list_object

    def get_objects_by_filters(self, begin_date=None, end_date=None, adults=1):
        path_url = "/apartments"
        logging.info(self.url + path_url)
        list_object: list[models.Apartment] = []
        page = 1
        while True:
            response = requests.post(
                self.url + path_url,
                json={
                    "begin_date": begin_date,
                    "end_date": end_date,
                    "guests": {
                        "adults": adults,
                        "children": []
                    },
                    "apartment_ids": [],
                    "page": page
                }
            )

            if response.status_code == 404:
                return ConnectionError("Not founded resources")

            if response.status_code in (500, 501, 505):
                return ConnectionError("Error with realtycalendar. Check access")

            raw_data = response.json().get("apartments")
            if raw_data in (None, []):
                break

            for raw_object in raw_data:
                serialized_object = models.Apartment(**raw_object)
                list_object.append(serialized_object)

            page += 1
        return list_object


# rc = RealtyCalendar("https://realtycalendar.ru/v2/widget/AAAwUw")
# data = rc.get_objects_by_filters(
#     begin_date="2025-04-12",
#     end_date="2025-04-27"
# )
# pprint.pprint(data)