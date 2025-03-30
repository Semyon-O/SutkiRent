from django.contrib import admin
from .models import Article, MediaFile

# Регистрация моделей в административной панели

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'short_description')  # Поля, отображаемые в списке статей
    search_fields = ('title', 'content')  # Поля для поиска
    readonly_fields = ('publication_date',)  # Поля, доступные только для просмотра


class MediaFileAdmin(admin.TabularInline):
    model = MediaFile
    extra = 1  # Отключает создание пустых форм


class ArticleAdminWithMedia(admin.ModelAdmin):
    inlines = [MediaFileAdmin]
    list_display = ('title', 'publication_date', 'short_description')  # Поля, отображаемые в списке статей
    search_fields = ('title', 'content')  # Поля для поиска
    readonly_fields = ('publication_date',)  # Поля, доступные только для просмотра


# Регистрировать модель Article с новыми настройками
admin.site.unregister(Article)
admin.site.register(Article, ArticleAdminWithMedia)