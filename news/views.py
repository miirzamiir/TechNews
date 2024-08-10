from . import models, serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class NewsViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags', ]
    pagination_class = PageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
