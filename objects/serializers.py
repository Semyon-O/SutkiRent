from rest_framework import serializers
from . import models


class ObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Object
        fields = '__all__'

