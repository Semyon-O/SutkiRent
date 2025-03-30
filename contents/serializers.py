from rest_framework import serializers
from .models import Article, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    media = MediaFileSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'publication_date', 'short_description', 'media']