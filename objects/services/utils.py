from django.core.exceptions import ObjectDoesNotExist

from objects.models import *


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
                id=data['region'].get('name'),
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
                print(photo.url, obj)
                UrlObjectMedia(
                    url=photo.url,
                    object=obj
                ).save()

        return obj

    except Exception as e:
        raise Exception(f"Error creating/updating object: {str(e)}")


import time
import logging
from functools import wraps


def measure_time(func):
    """Декоратор для замера времени выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Начало замера
        start_time = time.perf_counter()

        # Вызов оригинальной функции
        result = func(*args, **kwargs)

        # Конец замера
        elapsed_time = time.perf_counter() - start_time

        # Формируем информацию о вызове
        func_name = func.__name__
        module_name = func.__module__
        full_name = f"{module_name}.{func_name}" if module_name else func_name

        # Логируем результат
        logging.info(f"⏱️ Функция {full_name} выполнилась за {elapsed_time:.4f} секунд")
        print(f"⏱️ [TIME] {full_name}(): {elapsed_time:.4f}s")  # Дублируем в консоль

        return result

    return wrapper