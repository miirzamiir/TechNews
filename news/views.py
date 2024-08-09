from rest_framework.viewsets import ReadOnlyModelViewSet
from . import models
from . import serializers


class NewsViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
