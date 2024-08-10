from ..models import Tag, News
from ..serializers import TagSerializer, NewsSerializer
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

# Tests for serializers.py
class TagSerializerTest(TestCase):

    def test_tag_serialization(self):
        persian_tag = Tag.objects.create(tag_label="تگ")
        english_tag = Tag.objects.create(tag_label="tag")
        special_char_tag = Tag.objects.create(tag_label="T1(g)ی")
        
        serializer = TagSerializer([persian_tag, english_tag, special_char_tag], many=True)

        self.assertEqual(serializer.data[0], {"id": persian_tag.id, "tag_label": "تگ"})
        self.assertEqual(serializer.data[1], {"id": english_tag.id, "tag_label": "tag"})
        self.assertEqual(serializer.data[2], {"id": special_char_tag.id, "tag_label": "T1(g)ی"})

    def test_invalid_tag_serialization(self):
        invalid_tag = Tag(tag_label="")
        serializer = TagSerializer(data=invalid_tag.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tag_label', serializer.errors)


class NewsSerializerTest(TestCase):

    def setUp(self):
        self.persian_tag = Tag.objects.create(tag_label="اخبار")
        self.english_tag = Tag.objects.create(tag_label="news")
        self.special_char_tag = Tag.objects.create(tag_label="N3(w)ی")
        
        self.persian_news = News.objects.create(
            title="نام خبر",
            text="این یک خبر غیرواقعی برای تست مدل است.",
            resource="http://fakenews1.com/"
        )
        self.english_news = News.objects.create(
            title="Fake News Title",
            text="This is a fake news for testing purposes.",
            resource="http://fakenews2.com/"
        )
        self.special_char_news = News.objects.create(
            title="N3(w)ی",
            text="Th!s is @noth3r f@ke new$.",
            resource="http://example.com/fake"
        )

        self.persian_news.tags.add(self.persian_tag)
        self.english_news.tags.add(self.english_tag)
        self.special_char_news.tags.add(self.special_char_tag)

    def test_news_serialization(self):
        serializer = NewsSerializer([self.persian_news, self.english_news, self.special_char_news], many=True)

        self.assertEqual(serializer.data[0], {
            "id": self.persian_news.id,
            "title": "نام خبر",
            "text": "این یک خبر غیرواقعی برای تست مدل است.",
            "resource": "http://fakenews1.com/",
            "tags": [
                {
                    "id": self.persian_tag.id,
                    "tag_label": "اخبار"
                }
            ]
        })
        self.assertEqual(serializer.data[1], {
            "id": self.english_news.id,
            "title": "Fake News Title",
            "text": "This is a fake news for testing purposes.",
            "resource": "http://fakenews2.com/",
            "tags": [
                {
                    "id": self.english_tag.id,
                    "tag_label": "news"
                }
            ]
        })
        self.assertEqual(serializer.data[2], {
            "id": self.special_char_news.id,
            "title": "N3(w)ی",
            "text": "Th!s is @noth3r f@ke new$.",
            "resource": "http://example.com/fake",
            "tags": [
                {
                    "id": self.special_char_tag.id,
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


