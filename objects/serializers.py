from rest_framework import serializers
from . import models


class ObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Object
        fields = '__all__'


class ShortObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Object
        fields = [
            'id',
            'url_path',
            'is_showing',
            'short_name',
            'cost',
            'banner',
            'city',
        ]