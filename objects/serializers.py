from rest_framework import serializers
from . import models

class TypeObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeObject
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'



class MetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metro
        fields = '__all__'


class ObjectServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectServices
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'


class ObjectMediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectsMediaFile
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = '__all__'


class ObjectInventorySerializer(serializers.ModelSerializer):

    inventory = InventorySerializer()

    class Meta:
        model = models.ObjectInventory
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'

class ObjectSerializer(serializers.ModelSerializer):

    object_inventories = ObjectInventorySerializer(source="objectinventory_set",many=True)
    services = ServiceSerializer(many=True)
    media = ObjectMediaFileSerializer(many=True, read_only=True)
    banner = BannerSerializer(many=False)
    near_metro = MetroSerializer(many=True)


    class Meta:
        model = models.Object
        fields = [
            'pk',
            'short_name',
            'cost',
            'type',
            'amount_rooms',
            'floor',
            'sleeps',
            # 'category',
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
            'near_metro',
            'media',
        ]


class ShortObjectSerializer(serializers.ModelSerializer):
    banner = BannerSerializer(many=False)
    near_metro = MetroSerializer(many=True)

    class Meta:
        model = models.Object
        fields = [
            'pk',
            'short_name',
            'cost',
            'type',
            'amount_rooms',
            'sleeps',
            'floor',
            #'category',
            'region',
            'city',
            'banner',
            'space',
            'address',
            'near_metro',
            'media',
        ]

