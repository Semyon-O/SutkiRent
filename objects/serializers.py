from rest_framework import serializers
from . import models

class TypeObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeObject
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'



class MetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metro
        fields = '__all__'


class ObjectServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectServices
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'


class ObjectMediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectsMediaFile
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = '__all__'


class ObjectInventorySerializer(serializers.ModelSerializer):

    inventory = InventorySerializer()

    class Meta:
        model = models.ObjectInventory
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'


class UnifiedMediaSerializer(serializers.Serializer):
    """Сериализатор, объединяющий MediaFile и UrlObjectMedia."""
    source_type = serializers.CharField()  # "file" или "url"
    url = serializers.URLField()

    class Meta:
        fields = ['source_type', 'url']

    @staticmethod
    def get_media_data(obj: 'models.UrlObjectMedia | models.ObjectsMediaFile'):
        """Преобразует объект в единый формат."""
        if isinstance(obj, models.UrlObjectMedia):  # Проверка на внешнюю ссылку
            return {
                'source_type': 'url',
                'url': obj.url,  # Внешний URL
            }
        elif isinstance(obj, models.ObjectsMediaFile):  # Проверка на файл
            return {
                'source_type': 'file',
                'url': obj.file.url,  # URL файла на сервере
            }
        return None


class ObjectSerializer(serializers.ModelSerializer):

    object_inventories = ObjectInventorySerializer(source="objectinventory_set",many=True)
    services = ServiceSerializer(many=True)
    all_media = serializers.SerializerMethodField()
    banner = BannerSerializer(many=False)
    near_metro = MetroSerializer(many=True)

    def get_all_media(self, obj: models.Object):
        file_medias = obj.file_media.all()
        url_medias = obj.url_media.all()

        unified_media = []
        for media in list(file_medias) + list(url_medias):
            data = UnifiedMediaSerializer.get_media_data(media)
            if data:
                unified_media.append(data)

        return unified_media

    class Meta:
        model = models.Object
        fields = [
            'pk',
            'short_name',
            'cost',
            'type',
            'amount_rooms',
            'floor',
            'sleeps',
            'capacity',
            # 'category',
            'region',
            'city',
            'banner',
            'space',
            'address',
            'description',
            'conditions_accommodation',
            'contacts',
            'finding_description',
            'helpful_info',
            'parking_info',
            'object_inventories',
            'services',
            'near_metro',
            'all_media',
        ]


class ShortObjectSerializer(serializers.ModelSerializer):
    banner = BannerSerializer(many=False)
    near_metro = MetroSerializer(many=True)
    media = serializers.SerializerMethodField()

    def get_media(self, obj: models.Object):

        file_media = obj.file_media.first()
        if file_media:
            return UnifiedMediaSerializer.get_media_data(file_media)

        url_media = obj.url_media.first()
        if url_media:
            return UnifiedMediaSerializer.get_media_data(url_media)

        return None

    class Meta:
        model = models.Object
        fields = [
            'pk',
            'short_name',
            'cost',
            'type',
            'amount_rooms',
            'sleeps',
            'floor',
            'capacity',
            #'category',
            'region',
            'city',
            'banner',
            'space',
            'address',
            'near_metro',
            'media'
        ]

