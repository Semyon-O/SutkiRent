import logging

import django_filters
from .models import Object, Region, TypeObject, Metro, Inventory, Service, ViewFromWindow, Bathroom, Accessibility


class ObjectFilter(django_filters.FilterSet):
    # Все ваши фильтры остаются без изменений
    cost = django_filters.RangeFilter(field_name='cost', method='filter_cost')
    type = django_filters.ModelChoiceFilter(queryset=TypeObject.objects.all())
    amount_rooms = django_filters.RangeFilter(field_name="amount_rooms")
    floor = django_filters.RangeFilter(field_name="floor")
    region = django_filters.ModelChoiceFilter(queryset=Region.objects.all())
    city = django_filters.CharFilter(lookup_expr='icontains')
    space = django_filters.RangeFilter(field_name='space')
    amount_sleeps = django_filters.RangeFilter(field_name='amount_sleeps')
    view_from_window = django_filters.ModelChoiceFilter(
        field_name='view_from_window',
        queryset=ViewFromWindow.objects.all(),
    )
    bathroom = django_filters.ModelChoiceFilter(
        field_name='bathroom',
        queryset=Bathroom.objects.all(),
    )
    near_metro = django_filters.ModelMultipleChoiceFilter(
        field_name="near_metro",
        queryset=Metro.objects.all()
    )
    inventories = django_filters.ModelMultipleChoiceFilter(
        field_name="inventories",
        queryset=Inventory.objects.all()
    )

    services = django_filters.ModelMultipleChoiceFilter(
        field_name="services",
        queryset=Service.objects.all()
    )
    accessibility = django_filters.ModelMultipleChoiceFilter(
        field_name='accessibility',
        queryset=Accessibility.objects.all()
    )

    booking_date = django_filters.DateFromToRangeFilter(
        label="Даты заезда/выезда",
        method='filter_by_booking_dates'
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_date_filter = any(
            f'booking_date{sep}' in self.data
            for sep in ['', '_after', '_before']
        )

    class Meta:
        model = Object
        fields = ['cost', 'type', 'amount_rooms', 'floor', 'region', 'city', 'space', 'booking_date']


    def filter_cost(self, queryset, name, value):
        """Кастомный фильтр по цене с учётом сценария"""
        if self.has_date_filter:
            return queryset

        return super().filter(name, value)

    def filter_by_booking_dates(self, queryset, name, value):
        """Заглушка"""
        return queryset
