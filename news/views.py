from . import models, serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class NewsViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ('title', 'text')
    filterset_fields = ['tags', ]
    pagination_class = PageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    filter_backends = [SearchFilter,]
    search_fields = ('tag_label', )
    pagination_class = PageNumberPagination