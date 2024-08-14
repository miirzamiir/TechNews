from . import models, serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class NewsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving news data. Providing listing,
    filtering, and searching of news list and read-only access to news items.

    Attributes:
        serializer_class: Serializer for news data.
        queryset: Queryset for retrieving all news items.
        filter_backends: Filters for searching and filtering news items.
        search_fields: Fields for searching in the news items.
        filterset_fields: Fields for filtering news items.
        pagination_class: Control the pagination of the news list.
    """
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ('title', 'text')
    filterset_fields = ['tags', ]
    pagination_class = PageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving tag data. Providing listing
    and searching of tag entries and read-only access to tags.

    Attributes:
        serializer_class: Serializer for tag data.
        queryset: Queryset for retrieving all tag items.
        filter_backends: Filters for searching tag items.
        search_fields: Fields for searching in the tag items.
        pagination_class: Control the pagination of the tag list.
    """
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    filter_backends = [SearchFilter,]
    search_fields = ('tag_label', )
    pagination_class = PageNumberPagination