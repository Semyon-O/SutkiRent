from django.contrib import admin

from . import models


admin.site.register(models.Object)
admin.site.register(models.Region)
admin.site.register(models.Banner)
admin.site.register(models.Category)
admin.site.register(models.TypeObject)
