from . import models
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model. Converts Tag model items into a dictionary.

    Meta:
        model: The model being serialized.
        fields: Fields to include in the serialization process.
    """
    class Meta:
        model = models.Tag
        fields = ('id', 'tag_label')


class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for the News model. Includes nested serialization for tags
    related to a news item. Converts News model items into a dictionary.

    Attributes:
        tags: Nested serializer for the tags related to the news item.

    Meta:
        model: The model being serialized.
        fields: Fields to include in the serialization process.
    """
    tags = TagSerializer(many=True)

    class Meta:
        model = models.News
        fields = ('id', 'title', 'text', 'resource', 'tags')