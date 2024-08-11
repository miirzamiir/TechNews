from . import models
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id', 'tag_label')


class NewsSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        model = models.News
        fields = ('id', 'title', 'text', 'resource', 'tags')