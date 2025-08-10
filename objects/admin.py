from django.contrib import admin

from . import models

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