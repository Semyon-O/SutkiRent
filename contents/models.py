from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

# Модель для хранения медиафайлов
class MediaFile(models.Model):
    file = models.FileField(upload_to='content/', verbose_name=_('Файл'))
    article = models.ForeignKey(
        'Article', on_delete=models.CASCADE, related_name='media'
    )

    def __str__(self):
        return f"{self.file.name}"


# Модель статьи
class Article(models.Model):
    title = models.CharField(_('Заголовок'), max_length=255)
    content = RichTextField(_('Описание'))
    publication_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)
    short_description = models.TextField(_('Краткое описание'), blank=True)

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')

    def __str__(self):
        return self.title