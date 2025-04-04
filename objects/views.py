from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
import django_filters

from . import models, filters
from . import serializers
from . import models


class ListObjects(ListAPIView):
    serializer_class = serializers.ShortObjectSerializer
    queryset = models.Object.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.ObjectFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


class RetrieveObject(RetrieveAPIView):

    serializer_class = serializers.ObjectSerializer
    queryset = models.Object.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = models.Object.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class TypeObjectListAPIView(ListAPIView):
    queryset = models.TypeObject.objects.all()
    serializer_class = serializers.TypeObjectSerializer


class CategoryListAPIView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CategoryRetrieveAPIView(RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class RegionListAPIView(ListAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer

class RegionRetrieveAPIView(RetrieveAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class BannerListAPIView(ListAPIView):
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerSerializer

class BannerRetrieveAPIView(RetrieveAPIView):
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerSerializer

class ServiceListAPIView(ListAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class ServiceRetrieveAPIView(RetrieveAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class InventoryListAPIView(ListAPIView):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer

class InventoryRetrieveAPIView(RetrieveAPIView):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer

class MetroListAPIView(ListAPIView):
    queryset = models.Metro.objects.all()
    serializer_class = serializers.MetroSerializer

class MetroRetrieveAPIView(RetrieveAPIView):
    queryset = models.Metro.objects.all()
    serializer_class = serializers.MetroSerializer

class ObjectServicesListAPIView(ListAPIView):
    queryset = models.ObjectServices.objects.all()
    serializer_class = serializers.ObjectServicesSerializer

class ObjectServiceRetrieveAPIView(RetrieveAPIView):
    queryset = models.ObjectServices.objects.all()
    serializer_class = serializers.ObjectServicesSerializer

class ObjectInventoryListAPIView(ListAPIView):
    queryset = models.ObjectInventory.objects.all()
    serializer_class = serializers.ObjectInventorySerializer

class ObjectInventoryRetrieveAPIView(RetrieveAPIView):
    queryset = models.ObjectInventory.objects.all()
    serializer_class = serializers.ObjectInventorySerializer