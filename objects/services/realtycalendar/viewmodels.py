import datetime
import logging
import pprint
from typing import List

import requests
from . import models
from .models import ObjectCalendar


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

    def get_objects_by_filters(self, begin_date=None, end_date=None, adults=1, page=None):
        path_url = "/apartments"
        logging.info(self.url + path_url)
        list_object: list[models.Apartment] = []

        if page != None:
            return self.get_objects_by_page(begin_date, end_date, adults, page)

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
                try:
                    serialized_object = models.Apartment(**raw_object)
                    list_object.append(serialized_object)
                except Exception:
                    pass

            page += 1

        return list_object

    def get_objects_by_page(self, begin_date=None, end_date=None, adults=1, page=0):
        path_url = "/apartments"
        logging.info(self.url + path_url)
        list_object: list[models.Apartment] = []
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
        for raw_object in raw_data:
            try:
                serialized_object = models.Apartment(**raw_object)
                list_object.append(serialized_object)
            except Exception:
                pass

        return list_object

    def get_object_date(self, object_id: int, begin_date="2025-01-01", end_date="2025-12-31") -> List[ObjectCalendar]:
        path_url = "/calendar"
        payload = {
            "apartment_id": str(object_id),
            "begin_date": str(begin_date),
            "end_date": str(end_date),
            "guests": {
                "adults": 1,
                "children": []
            }
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "insomnia/11.0.2"
        }

        response = requests.request("POST", self.url+path_url, json=payload, headers=headers)

        raw_dates = response.json()
        list_object_date = []
        for date in raw_dates.get("calendar", []):
            try:
                serialized_object = models.ObjectCalendar(**date)
                list_object_date.append(serialized_object)
            except Exception as e:
                print(e)
        return list_object_date