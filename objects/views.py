from http.client import responses

from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
import django_filters

from . import models, filters
from . import serializers
from .models import Object


class ListObjects(ListAPIView):
    serializer_class = serializers.ObjectSerializer
    queryset = Object.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.ObjectFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response