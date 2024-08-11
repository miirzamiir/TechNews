from ..models import Tag, News
from ..serializers import TagSerializer, NewsSerializer
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

# Tests for serializers.py
class TagSerializerTest(TestCase):

    def test_tag_serialization(self):
        tag = Tag.objects.create(tag_label="T1(g)ی")
        serializer = TagSerializer(tag)
        self.assertEqual(serializer.data, {"id": tag.id, "tag_label": "T1(g)ی"})

    def test_invalid_tag_serialization(self):
        invalid_tag = Tag(tag_label="")
        serializer = TagSerializer(data=invalid_tag.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tag_label', serializer.errors)
    
    def test_tag_update_serialization(self):
        tag = Tag.objects.create(tag_label="initial_tag")
        data = {"tag_label": "updated_tag"}
        serializer = TagSerializer(tag, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_tag = serializer.save()
        self.assertEqual(updated_tag.tag_label, "updated_tag")
    
    def test_tag_bulk_creation_deserialization(self):
        data = [
            {"tag_label": "bulk_tag_1"},
            {"tag_label": "bulk_tag_2"},
            {"tag_label": "bulk_tag_3"}
        ]
        serializer = TagSerializer(data=data, many=True)
        self.assertTrue(serializer.is_valid())
        tags = serializer.save()
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0].tag_label, "bulk_tag_1")
        self.assertEqual(tags[1].tag_label, "bulk_tag_2")
        self.assertEqual(tags[2].tag_label, "bulk_tag_3")


class NewsSerializerTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(tag_label="N3(w)ی")
        self.news = News.objects.create(
            title="N3(w)ی",
            text="Th!s is @noth3r f@ke new$.",
            resource="http://example.com/fake"
        )
        self.news.tags.add(self.tag)

    def test_news_serialization(self):
        serializer = NewsSerializer(self.news)
        self.assertEqual(serializer.data, {
            "id": self.news.id,
            "title": "N3(w)ی",
            "text": "Th!s is @noth3r f@ke new$.",
            "resource": "http://example.com/fake",
            "tags": [
                {
                    "id": self.tag.id,
                    "tag_label": "N3(w)ی"
                }
            ]
        })

    def test_title_invalid_news_serialization(self):
        invalid_news = News(
            title="",  # Invalid because title is empty
            text="some text.",
            resource="http://valid-url.com"  
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_text_invalid_news_serialization(self):
        invalid_news = News(
            title="title",  
            text="",    # Invalid because text is empty
            resource="http://valid-url.com"  
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

    def test_resource_invalid_news_serialization(self):
        invalid_news = News(
            title="title",  
            text="some text.",
            resource="invalid-url"  # Invalid url
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('resource', serializer.errors)


