from rest_framework import serializers
from . import models


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        fields = ['name']


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = ['name']


class ObjectInventorySerializer(serializers.ModelSerializer):

    inventory = InventorySerializer()

    class Meta:
        model = models.ObjectInventory
        fields = ['inventory', 'amount']


class ObjectSerializer(serializers.ModelSerializer):

    object_inventories = ObjectInventorySerializer(source="objectinventory_set",many=True)
    services = ServiceSerializer(many=True)

    class Meta:
        model = models.Object
        fields = [
            'pk',
            'short_name',
            'cost',
            'type',
            'amount_rooms',
            'floor',
            'category',
            'region',
            'city',
            'banner',
            'space',
            'address',
            'description',
            'conditions_accommodation',
            'contacts',
            'finding_description',
            'helpful_info',
            'parking_info',
            'object_inventories',
            'services',
            'near_metros',
        ]

