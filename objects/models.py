from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

class TypeObject(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Тип объекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Типы объектов'
        verbose_name = 'Тип объекта'
        ordering = ['name']
        db_table = 'types'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['name']
        db_table = 'categories'

class Region(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Регион')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Регионы'
        verbose_name = 'Регион'
        ordering = ['name']
        db_table = 'regions'


class Banner(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Баннер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Баннеры'
        verbose_name = 'Баннер'
        ordering = ['name']
        db_table = 'banners'


class Object(models.Model):
    # id
    is_showing = models.BooleanField(default=True, db_index=True, verbose_name='Опубликовать?')
    short_name = models.CharField(max_length=255, verbose_name='Короткое имя')
    cost = models.IntegerField(db_index=True, verbose_name='Стоимость базовая')
    type = models.ForeignKey(to=TypeObject, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Тип')
    amount_rooms = models.IntegerField(verbose_name="Количество комнат", null=True, blank=True, db_index=True)
    amount_sleeps = models.IntegerField(verbose_name='Количество спальных мест (количество)', null=True, blank=True, db_index=True)
    sleeps = models.CharField(max_length=255, verbose_name="Количество спальных мест (описание)", null=True)
    capacity = models.IntegerField(verbose_name="Количество людей", null=True)
    floor = models.IntegerField(default=1, verbose_name="Этаж", null=True, db_index=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Категория')
    region = models.ForeignKey(to=Region, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name="Регион")
    city = models.CharField(max_length=255, null=True, db_index=True, blank=True, verbose_name='Город')
    banner = models.ForeignKey(to=Banner, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Баннер')
    space = models.FloatField(null=True, db_index=True, blank=True, verbose_name='Площадь')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    description = RichTextField(null=True, blank=True, verbose_name='Описание')
    conditions_accommodation = RichTextField(null=True, blank=True, verbose_name='Условия заселения')
    contacts = RichTextField(null=True, blank=True, verbose_name='Контактные данные')
    finding_description = RichTextField(null=True, blank=True, verbose_name='Как найти')
    helpful_info = RichTextField(null=True, blank=True, verbose_name='Полезная информация')
    parking_info = RichTextField(null=True, blank=True, verbose_name='Информация по парковке')
    near_metro = models.ManyToManyField(to='Metro', db_index=True, null=True, through='NearMetroObject', verbose_name=_("Метро у объекта"))

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    view_from_window = models.ForeignKey(to='ViewFromWindow', on_delete=models.SET_NULL,db_index=True, null=True, blank=True, verbose_name=_("Вид из окна"))
    bathroom = models.ForeignKey(to='Bathroom', on_delete=models.SET_NULL, db_index=True, null=True, blank=True, verbose_name=_("Тип ванной комнаты"))

    services = models.ManyToManyField('Service', through='ObjectServices', verbose_name=_("Услуги для объекта"))
    inventories = models.ManyToManyField('Inventory', through='ObjectInventory', verbose_name=_("Инвентарь для объекта"))
    accessibility = models.ManyToManyField('Accessibility', through='ObjectAccessibilities', verbose_name=_("Специальный возможности объекта"))

    def __str__(self):
        return f"{self.short_name} ({self.pk})"

    class Meta:
        verbose_name_plural = 'Объекты'
        verbose_name = 'Объект'
        db_table = 'objects'


# Модель для хранения медиафайлов
class ObjectsMediaFile(models.Model):
    file = models.FileField(upload_to='objects/images', verbose_name=_('Файл'), null=True, blank=True)
    object = models.ForeignKey(
        Object, on_delete=models.CASCADE, related_name='file_media'
    )

    def __str__(self):
        return self.file.name


class UrlObjectMedia(models.Model):
    url = models.URLField(verbose_name=_('URL изображения'))
    object = models.ForeignKey(
        Object, on_delete=models.CASCADE, related_name='url_media'
    )
    is_external = models.BooleanField(default=True, verbose_name=_('Внешний ресурс'))

    def __str__(self):
        return self.url


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Идентификатор услуги')
    title_to_show = models.CharField(max_length=255, verbose_name="Услуга отб.на сайте", null=True, blank=True)
    icon = models.FileField(verbose_name="Иконка", null=True, blank=True, upload_to='objects/services/icons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Услуги'
        verbose_name = 'Услуга'
        ordering = ['name']
        db_table = 'services'


class Inventory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Инвентарь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Инвентарь'
        verbose_name = 'Инвентарь'
        ordering = ['name']
        db_table = 'inventories'


class Metro(models.Model):
    name = models.CharField(max_length=255,primary_key=True)

    def __str__(self):
        return self.name


class NearMetroObject(models.Model):
    metro = models.ForeignKey(to=Metro, on_delete=models.SET_NULL, null=True, verbose_name=_("Метро"))
    object = models.ForeignKey(to=Object, on_delete=models.SET_NULL, null=True, verbose_name=_("Объект"))

class ObjectServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="Объект")

    def __str__(self):
        return f"{self.service} - {self.object}"

    class Meta:
        verbose_name_plural = "Услуги для объекта"
        verbose_name = "Услуга для объекта"
        ordering = ['service', 'object']

class ObjectInventory(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="Объект")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name="Наименование инвентаря")
    amount = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.inventory} - {self.object}"

    class Meta:
        verbose_name_plural = "Инвентарь для объекта"
        verbose_name = "Инвентарь для объекта"
        ordering = ['object', 'inventory']

class ObjectAccessibilities(models.Model):
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, null=True)
    accessibility_type = models.ForeignKey('Accessibility', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Специальные возможности для объектов"
        verbose_name = "Спец. возможность для объекта"


class ViewFromWindow(models.Model):
    notation_view = models.CharField(max_length=255,
                                     db_index=True,
                                     verbose_name=_("Вид из окна"))

    class Meta:
        verbose_name_plural = "Виды из окон"
        verbose_name = "Вид из окна"

    def __str__(self):
        return str(self.notation_view)

class Accessibility(models.Model):
    accessibility_type = models.CharField(max_length=255,
                                          db_index=True,
                                          null=True,
                                          verbose_name=_("Специальный возможности"))

    class Meta:
        verbose_name_plural = "Специальные возможности"
        verbose_name = "Спец. возможность"

    def __str__(self):
        return str(self.accessibility_type)


class Bathroom(models.Model):
    bathroom_type = models.CharField(max_length=255,
                                     db_index=True,
                                     verbose_name=_("Тип ванной комнаты"))

    class Meta:
        verbose_name_plural = "Типы ванных комнат"
        verbose_name = "Тип ванной"

    def __str__(self):
        return str(self.bathroom_type)