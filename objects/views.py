from rest_framework import generics
from rest_framework.response import Response

from . import models
from . import serializers


class ListObjects(generics.ListAPIView):

    queryset = models.Object.objects.all()
    serializer_class = serializers.ShortObjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.ShortObjectSerializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveObject(generics.RetrieveAPIView):

    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs)
        return response