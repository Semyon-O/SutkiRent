import django_filters
from .models import Object, Region, Category, TypeObject, Metro


class ObjectFilter(django_filters.FilterSet):
    cost = django_filters.RangeFilter(field_name='cost')
    type = django_filters.ModelChoiceFilter(queryset=TypeObject.objects.all())
    amount_rooms = django_filters.RangeFilter(field_name="amount_rooms")
    floor = django_filters.RangeFilter(field_name="floor")
    region = django_filters.ModelChoiceFilter(queryset=Region.objects.all())
    city = django_filters.CharFilter(lookup_expr='icontains')
    space = django_filters.RangeFilter(field_name='space')
    near_metro = django_filters.ModelMultipleChoiceFilter(field_name="near_metro",
                                                          queryset=Metro.objects.all())

    booking_date = django_filters.DateFromToRangeFilter(field_name='booking_date', lookup_expr='icontains')

    class Meta:
        model = Object
        fields = ['cost', 'type', 'amount_rooms', 'floor', 'region', 'city', 'space']