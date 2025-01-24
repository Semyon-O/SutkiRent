from django.contrib import admin

from . import models


class ServicesObjectInlines(admin.TabularInline):
    model = models.ObjectServices
    extra = 3

class InventoryObjectInline(admin.TabularInline):
    model = models.ObjectInventory
    extra = 3

@admin.register(models.Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [ServicesObjectInlines,InventoryObjectInline]


admin.site.register(models.Region)
admin.site.register(models.Banner)
admin.site.register(models.Category)
admin.site.register(models.TypeObject)
admin.site.register(models.ObjectServices)
admin.site.register(models.Service)
admin.site.register(models.Inventory)
admin.site.register(models.ObjectInventory)
