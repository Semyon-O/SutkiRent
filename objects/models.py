from django.db import models


class TypeObject(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Region(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Banner(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Object(models.Model):
    url_path = models.CharField(unique=True, max_length=255)
    is_showing = models.BooleanField(default=True, db_index=True)
    short_name = models.CharField(max_length=255)
    cost = models.IntegerField(db_index=True)
    type = models.ForeignKey(to=TypeObject, on_delete=models.SET_NULL, null=True, db_index=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, db_index=True)
    city = models.CharField(max_length=255, null=True, db_index=True)
    banner = models.ForeignKey(to=Banner, on_delete=models.SET_NULL, null=True, db_index=True)
    space = models.FloatField(null=True, db_index=True)
    description = models.TextField(null=True)
    conditions_accommodation = models.TextField(null=True)
    contacts = models.TextField(null=True)
    finding_description = models.TextField(null=True)
    helpful_info = models.TextField(null=True)
    parking_info = models.TextField(null=True)

    services = models.ManyToManyField('Service', through='ObjectServices')
    inventories = models.ManyToManyField('Inventory', through='ObjectInventory')

class Service(models.Model):
    name = models.CharField(max_length=255)


class Inventory(models.Model):
    name = models.CharField(max_length=255)


class ObjectServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)


class ObjectInventory(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    amount = models.IntegerField()