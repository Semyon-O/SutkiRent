import datetime
import logging
import typing
from pprint import pprint

from core.settings import RC
from objects.models import *
from objects.services import realtycalendar


def create_or_update_object(data: [dict]):
    """
    Создает или обновляет объект Object и связанные модели
    :param data: словарь с данными для объекта
    :return: созданный/обновленный объект Object
    """
    try:
        # Обрабатываем ForeignKey поля
        type_obj = None
        if data.get('type'):
            type_obj, _ = TypeObject.objects.get_or_create(
                name=data['type'].get('name'),
            )

        category_obj = None
        if data.get('category'):
            category_obj, _ = Category.objects.get_or_create(
                name=data['category'].get('name'),
                defaults=data['category']
            )

        region_obj = None
        if data.get('region'):
            region_obj, _ = Region.objects.get_or_create(
                id=data['region'].get('id'),
                defaults={
                    'id': data['region'].get('id'),
                    'name': data['region'].get('name')
                }
            )

        banner_obj = None
        if data.get('banner'):
            banner_obj, _ = Banner.objects.get_or_create(
                id=data['banner'].get('id'),
                defaults=data['banner']
            )


        # Создаем/обновляем основной объект
        obj, created = Object.objects.update_or_create(
            id=data.get('id'),  # если id нет - создаст новый объект
            defaults={
                'id': data.get('id'),
                'is_showing': data.get('is_showing', True),
                'short_name': data['short_name'],
                'cost': data['cost'],
                'type': type_obj,
                'amount_rooms': data.get('amount_rooms'),
                'sleeps': data.get('sleeps'),
                'capacity': data.get('capacity'),
                'floor': data.get('floor', 1),
                'category': category_obj,
                'region': region_obj,
                'city': data.get('city'),
                'banner': banner_obj,
                'space': data.get('space'),
                'address': data.get('address'),
                'description': data.get('description'),
                'conditions_accommodation': data.get('conditions_accommodation'),
                'contacts': data.get('contacts'),
                'finding_description': data.get('finding_description'),
                'helpful_info': data.get('helpful_info'),
                'parking_info': data.get('parking_info'),
                'latitude': data.get("latitude"),
                'longitude': data.get('longitude')
            }
        )

        # Обрабатываем ManyToMany поле near_metro
        if data.get('near_metro'):
            metro_objs = []
            for metro_data in data['near_metro']:
                metro, _ = Metro.objects.get_or_create(
                    name=metro_data.get('name'),
                )
                metro_objs.append(metro)
            obj.near_metro.set(metro_objs)

        if data.get('url_medias'):
            for photo in data['url_medias']:
                UrlObjectMedia(
                    url=photo.url,
                    object=obj
                ).save()

        return obj

    except Exception as e:
        raise Exception(f"Error creating/updating object: {str(e)}")

def import_objects_from_rc():

    rc_objects: list[realtycalendar.models.Apartment] = RC.get_all_objects()

    for rc_object in rc_objects:
        data = {
            'id': rc_object.id,
            'short_name': rc_object.title,
            'cost': rc_object.price.common.without_discount,
            'city': rc_object.city.title,
            'amount_rooms': rc_object.rooms,
            'address': rc_object.address,
            'description': rc_object.desc,
            'capacity': rc_object.capacity,
            'space': rc_object.area,
            'floor': rc_object.floor,
            'sleeps': rc_object.sleeps,
            'url_medias': rc_object.photos,
            'region': {
                'id': rc_object.city.id,
                'name': rc_object.city.title
            },
            'latitude': rc_object.coordinates.lat,
            'longitude': rc_object.coordinates.lon
        }
        try:
            create_or_update_object(data)
            logging.info('[INFO] Object<id={0} short_name={1}> imported successful '.format(rc_object.id, rc_object.title))
        except Exception as e:
            logging.error('[ERROR] Object<id={0} short_name={1}> imported error '.format(rc_object.id, rc_object.title))
            logging.exception(e)

def load_daily_price_per_object():
    objects = Object.objects.all()
    print(len(objects))
    for obj in objects:
        today = datetime.date.today()
        cur_year = today.year
        cur_month = today.month
        cur_day = today.day
        object_dates = RC.get_object_date(obj.pk,
                                          begin_date=f"{cur_year}-{cur_month}-{cur_day}",
                                          end_date=f"{cur_year + 1}-1-01")
        print(f"FOR OBJECT [{obj.pk}] ({cur_year}-{cur_month}-{cur_day} - {cur_year + 1}-1-01) THIS DATES")
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