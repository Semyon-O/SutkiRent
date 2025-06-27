import logging
from typing import List

from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
import django_filters

from core.settings import RC
from . import models, filters
from . import serializers
from . import models

from .services import realtycalendar, utils
from .services.realtycalendar.models import Apartment



# admin views
def import_objects(request):

    rc_objects: list[realtycalendar.models.Apartment] = RC.get_all_objects()

    for rc_object in rc_objects:
        data = {
            'id': rc_object.id,
            'short_name': rc_object.title,
            'cost': rc_object.price.common.without_discount,
            'city': rc_object.city.title,
            'amount_rooms': rc_object.rooms,
            'address': rc_object.address,
            'description': rc_object.desc,
            'capacity': rc_object.capacity,
            'space': rc_object.area,
            'floor': rc_object.floor,
            'sleeps': rc_object.sleeps,
            'url_medias': rc_object.photos,
            'region': {
                'id': rc_object.city.id,
                'name': rc_object.city.title
            },
            'latitude': rc_object.coordinates.lat,
            'longitude': rc_object.coordinates.lon
        }
        try:
            utils.create_or_update_object(data)
        except Exception as e:
            logging.exception(e)
    return HttpResponse(status=200)

def index(request):
    logging.log(logging.INFO, request.META)
    headers = str(request.META)
    a = RC.get_object_date(149542, begin_date="2025-07-01", end_date="2025-08-01")

    return HttpResponse(headers)

# GET /api/objects/?cost_min=&cost_max=&type=&amount_rooms_min=&amount_rooms_max=&floor_min=&floor_max=&region=&city=&space_min=&space_max=&booking_date_after=2025-04-13&booking_date_before=2025-04-17
# apis
class ListObjects(ListAPIView):
    serializer_class = serializers.ShortObjectSerializer
    queryset = models.Object.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.ObjectFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """Основной метод получения queryset с поэтапной фильтрацией"""
        queryset = super().get_queryset()
        # Фильтрация по данным из RealtyCalendar
        rc_apartments = self._get_filtered_rc_apartments()

        if rc_apartments:
            queryset = self._apply_rc_filters(queryset, rc_apartments)

        queryset = self.filter_queryset(queryset)

        # Добавляем данные о ценах
        if rc_apartments:
            queryset = self._enrich_with_prices(queryset, rc_apartments)
            return queryset

        return queryset

    def _get_filtered_rc_apartments(self) -> List[Apartment]:
        """Фильтрация данных из RealtyCalendar по датам и цене"""
        rc_apartments = self._filter_by_dates()


        if rc_apartments and ('cost_min' in self.request.query_params and 'cost_max' in self.request.query_params):
            rc_apartments = self._filter_by_price(rc_apartments)

        return rc_apartments

    def _filter_by_dates(self) -> List[Apartment]:
        """Фильтрация объектов по датам через API RealtyCalendar"""


        begin_date = self.request.query_params.get('booking_date_after')
        end_date = self.request.query_params.get('booking_date_before')
        page = self.request.query_params.get('page', None)

        rc = realtycalendar.viewmodels.RealtyCalendar("https://realtycalendar.ru/v2/widget/AAAwUw")

        if not (begin_date or end_date):
            return []

        try:
            return rc.get_objects_by_filters(
                begin_date=begin_date,
                end_date=end_date,
                page=page
            )

        except Exception as e:
            logging.error(f"RealtyCalendar API error: {str(e)}")
            return []

    def _filter_by_price(self, apartments: List[Apartment]) -> List[Apartment]:
        """Фильтрация объектов по стоимости"""
        price_min = self.request.query_params.get('cost_min')
        price_max = self.request.query_params.get('cost_max')
        try:
            if price_min or price_max:
                return Apartment.filter_by_price(
                    apartments,
                    price_min=float(price_min),
                    price_max=float(price_max)
                )
        except (ValueError, AttributeError) as e:
            logging.warning(f"Invalid cost parameter:. Error: {str(e)}")

        return apartments

    def _apply_rc_filters(self, queryset: QuerySet, rc_apartments: List[Apartment]) -> QuerySet:
        """Применение фильтров по ID из RealtyCalendar"""
        available_ids = [apt.id for apt in rc_apartments]
        return queryset.filter(id__in=available_ids)

    def _enrich_with_prices(self, queryset: QuerySet, rc_apartments: List[Apartment]) -> QuerySet:
        """Добавление актуальных цен к объектам"""
        price_map = {apt.id: apt.price.common.without_discount for apt in rc_apartments}
        for obj in queryset:
            if obj.id in price_map:
                obj.cost = price_map[obj.id]
        return queryset

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


class BathroomTypesList(ListAPIView):
    queryset = models.Bathroom.objects.all()
    serializer_class = serializers.BathroomTypesSerializer


class ViewFromWindowList(ListAPIView):
    queryset = models.ViewFromWindow.objects.all()
    serializer_class = serializers.ViewFromWindowSerializer

class AccessibilityTypes(ListAPIView):
    queryset = models.Accessibility.objects.all()
    serializer_class = serializers.AccessibilitySerializer