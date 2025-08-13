import logging
from django.contrib import messages

from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, reverse

from . import models
from .services import utils, realtycalendar


class MediaFileAdmin(admin.TabularInline):
    model = models.ObjectsMediaFile
    extra = 1

class URLObjectMediaAdmin(admin.TabularInline):
    model = models.UrlObjectMedia
    extra = 1

class ServicesObjectInlines(admin.TabularInline):
    model = models.ObjectServices
    extra = 3

class MetroObjectInlines(admin.TabularInline):
    model = models.NearMetroObject
    extra = 3

class InventoryObjectInline(admin.TabularInline):
    model = models.ObjectInventory
    extra = 3

class AccessibilitiesObject(admin.TabularInline):
    model = models.ObjectAccessibilities
    extra = 2

@admin.register(models.Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [ServicesObjectInlines,InventoryObjectInline,
               AccessibilitiesObject,
               MetroObjectInlines,
               MediaFileAdmin,
               URLObjectMediaAdmin,
            ]

    change_list_template = 'admin/objects/object/change_list.html'

    actions = ['make_published']
    search_fields = ('short_name', 'address', 'id')
    list_filter = ('category',
                   'region',
                   'banner',
                   'view_from_window',
                   'bathroom', )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.admin_site.admin_view(self.import_view), name='import_objects_from_rc'),
        ]
        return custom_urls + urls  # Важно: новые URL должны быть в начале, чтобы не перекрываться стандартными

    def import_view(self, request):
        if request.method == 'GET':
            RC = realtycalendar.viewmodels.RealtyCalendar("https://realtycalendar.ru/v2/widget/AAAwUw")
            try:
                rc_objects: list[realtycalendar.models.Apartment] = RC.get_all_objects()
            except ConnectionRefusedError:
                messages.warning(request, "Ресурсы не были найдены")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except ConnectionError:
                messages.error(request, "Сервис RC на данный момент не отвечает!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
                    messages.success(request, "Данные успешно обновлены!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                except ValueError as e:
                    logging.exception(e)
                    messages.error(request, "Ошибка при обновлении данных!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return HttpResponse("Неправильный запрос")

admin.site.register(models.Region)
admin.site.register(models.Banner)
admin.site.register(models.Category)
admin.site.register(models.TypeObject)
admin.site.register(models.ObjectServices)
admin.site.register(models.Service)
admin.site.register(models.Inventory)
admin.site.register(models.ObjectInventory)
admin.site.register(models.Metro)
admin.site.register(models.ViewFromWindow)
admin.site.register(models.Bathroom)
admin.site.register(models.Accessibility)
admin.site.register(models.ObjectAccessibilities)