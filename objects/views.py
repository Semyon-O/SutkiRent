from http.client import responses

from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView
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


class RetrieveObject(RetrieveAPIView):

    serializer_class = serializers.ObjectSerializer
    queryset = Object.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = models.Object.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
