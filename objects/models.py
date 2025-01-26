from django.db import models


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
    url_path = models.CharField(unique=True, max_length=255, verbose_name='Маршрут')
    is_showing = models.BooleanField(default=True, db_index=True, verbose_name='Опубликовать?')
    short_name = models.CharField(max_length=255, verbose_name='Короткое имя')
    cost = models.IntegerField(db_index=True, verbose_name='Стоимость')
    type = models.ForeignKey(to=TypeObject, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Тип')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Категория')
    city = models.CharField(max_length=255, null=True, db_index=True, blank=True, verbose_name='Город')
    banner = models.ForeignKey(to=Banner, on_delete=models.SET_NULL, null=True, db_index=True, blank=True, verbose_name='Баннер')
    space = models.FloatField(null=True, db_index=True, blank=True, verbose_name='Площадь')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    conditions_accommodation = models.TextField(null=True, blank=True, verbose_name='Условия заселения')
    contacts = models.TextField(null=True, blank=True, verbose_name='Контактные данные')
    finding_description = models.TextField(null=True, blank=True, verbose_name='Как найти')
    helpful_info = models.TextField(null=True, blank=True, verbose_name='Полезная информация')
    parking_info = models.TextField(null=True, blank=True, verbose_name='Информация по парковке')

    services = models.ManyToManyField('Service', through='ObjectServices')
    inventories = models.ManyToManyField('Inventory', through='ObjectInventory')

    def __str__(self):
        return f"{self.short_name} ({self.pk})"

    class Meta:
        verbose_name_plural = 'Объекты'
        verbose_name = 'Объект'
        db_table = 'objects'


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Услуги')

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


class ObjectServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)


class ObjectInventory(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    amount = models.IntegerField()