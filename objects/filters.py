import logging

import django_filters
from .models import Object, Region, TypeObject, Metro, ViewFromWindow, Bathroom, Service, Accessibility


class ObjectFilter(django_filters.FilterSet):
    # Все ваши фильтры остаются без изменений
    cost = django_filters.RangeFilter(field_name='cost', method='filter_cost')
    type = django_filters.ModelChoiceFilter(queryset=TypeObject.objects.all())
    amount_rooms = django_filters.RangeFilter(field_name="amount_rooms")
    floor = django_filters.RangeFilter(field_name="floor")
    region = django_filters.ModelChoiceFilter(queryset=Region.objects.all())
    city = django_filters.CharFilter(lookup_expr='icontains')
    space = django_filters.RangeFilter(field_name='space')
    near_metro = django_filters.ModelMultipleChoiceFilter(
        field_name="near_metro",
        queryset=Metro.objects.all()
    )

    view_from_window = django_filters.ModelChoiceFilter(
        field_name='view_from_window',
        queryset=ViewFromWindow.objects.all()
    )

    bathroom = django_filters.ModelChoiceFilter(
        field_name='bathroom',
        queryset=Bathroom.objects.all()
    )

    services = django_filters.ModelMultipleChoiceFilter(
        field_name = 'services',
        queryset=Service.objects.all()
    )

    accessibility = django_filters.ModelMultipleChoiceFilter(
        field_name = 'accessibility',
        queryset= Accessibility.objects.all()
    )

    booking_date = django_filters.DateFromToRangeFilter(
        label="Даты заезда/выезда",
        method='filter_by_booking_dates'
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = kwargs.get('data')

        self.has_date_filter = False
        if data.get('booking_date_after') not in ('', None) \
            and data.get("booking_date_before") not in ('', None):
            self.has_date_filter = True

    class Meta:
        model = Object
        fields = ['cost', 'type', 'amount_rooms', 'floor', 'region', 'city', 'space', 'booking_date']
    #
    # def filter_queryset(self, queryset):
    #     print(queryset)
    #     super().filter_queryset(queryset)
    #     # 1. Сначала применяем фильтр по датам (если он есть в запросе)
    #     if 'booking_date' in self.form.cleaned_data:
    #         booking_value = self.form.cleaned_data['booking_date']
    #         queryset = self.filter_by_booking_dates(queryset, 'booking_date', booking_value)
    #
    #     # 2. Затем применяем все остальные фильтры в стандартном порядке
    #     for name, value in self.form.cleaned_data.items():
    #         if name != 'booking_date' and value:
    #             queryset = self.filters[name].filter(queryset, value)
    #
    #     return queryset

    def filter_cost(self, queryset, name, value):
        """Кастомный фильтр по цене с учётом сценария"""
        if self.has_date_filter:
            return queryset
        # Стандартная логика диапазона
        if value.start is not None:
            queryset = queryset.filter(**{f"{name}__gte": value.start})
        if value.stop is not None:
            queryset = queryset.filter(**{f"{name}__lte": value.stop})
        return queryset

    def filter_by_booking_dates(self, queryset, name, value):
        """Заглушка"""
        return queryset
