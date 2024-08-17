from ..models import Tag, News
from ..serializers import TagSerializer, NewsSerializer
from django.test import TestCase
from django.utils import timezone
import pytz
from datetime import datetime


# Tests for serializers.py
class TagSerializerTest(TestCase):
    """
    TestCase for the TagSerializer. Contains unit tests to verify the serialization
    and deserialization behavior of the TagSerializer.
    """

    def test_tag_serialization(self):
        """Tests the serialization of a Tag instance into a dictionary."""
        tag = Tag.objects.create(tag_label="T1(g)ی")
        serializer = TagSerializer(tag)
        self.assertEqual(serializer.data, {"id": tag.id, "tag_label": "T1(g)ی"})

    def test_invalid_tag_serialization(self):
        """Tests the validation of an invalid Tag instance."""
        invalid_tag = Tag(tag_label="")
        serializer = TagSerializer(data=invalid_tag.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tag_label', serializer.errors)
    
    def test_tag_update_serialization(self):
        """Tests the partial update of a Tag instance using the serializer."""
        tag = Tag.objects.create(tag_label="initial_tag")
        data = {"tag_label": "updated_tag"}
        serializer = TagSerializer(tag, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_tag = serializer.save()
        self.assertEqual(updated_tag.tag_label, "updated_tag")
    
    def test_tag_bulk_creation_deserialization(self):
        """Tests the bulk creation of Tag instances from JSON data."""
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
    """
    TestCase for the NewsSerializer. Contains unit tests to verify the serialization
    and deserialization behavior of the NewsSerializer, including validation of its fields.

    Methods:
        setUp(): Sets up initial test data, including a Tag and a News instance.
        test_news_serialization(): Tests the serialization of a News instance into JSON format.
        test_title_invalid_news_serialization(): Tests the validation of an invalid News instance with an empty title.
        test_text_invalid_news_serialization(): Tests the validation of an invalid News instance with empty text.
        test_resource_invalid_news_serialization(): Tests the validation of an invalid News instance with an invalid resource URL.
    """

    def setUp(self):
        """Sets up initial test data, including a Tag and a News instance."""
        current_timezone = timezone.get_current_timezone()
        self.tag = Tag.objects.create(tag_label="N3(w)ی")
        self.news = News.objects.create(
            title="N3(w)ی",
            text="Th!s is @noth3r f@ke new$.",
            resource="http://example.com/fake",
            date=timezone.make_aware(datetime(1403, 3, 26, 9, 30), current_timezone)
        )
        self.news.tags.add(self.tag)

    def test_news_serialization(self):
        """Tests the serialization of a News instance into a dictionary."""
        serializer = NewsSerializer(self.news)
        self.assertEqual(serializer.data, {
            "id": self.news.id,
            "title": "N3(w)ی",
            "text": "Th!s is @noth3r f@ke new$.",
            "resource": "http://example.com/fake",
            "date": self.news.date.isoformat(),
            "tags": [
                {
                    "id": self.tag.id,
                    "tag_label": "N3(w)ی"
                }
            ]
        })
        print(serializer.data['date'])

    def test_title_invalid_news_serialization(self):
        """Tests the validation of an invalid News instance with an empty title."""
        invalid_news = News(
            title="",  # Invalid because title is empty
            text="some text.",
            resource="http://valid-url.com"  
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_text_invalid_news_serialization(self):
        """Tests the validation of an invalid News instance with empty text."""
        invalid_news = News(
            title="title",  
            text="",    # Invalid because text is empty
            resource="http://valid-url.com"  
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

    def test_resource_invalid_news_serialization(self):
        """Tests the validation of an invalid News instance with an invalid resource URL."""
        invalid_news = News(
            title="title",  
            text="some text.",
            resource="invalid-url"  # Invalid url
        )

        serializer = NewsSerializer(data=invalid_news.__dict__)
        self.assertFalse(serializer.is_valid())
        self.assertIn('resource', serializer.errors)

    def test_invalid_date_format_serialization(self):
        """Tests that the serializer raises a ValidationError for an invalid date format."""
        invalid_data = {
            "title": "Invalid Date Test",
            "text": "This news has an invalid date format.",
            "resource": "http://example.com/invalid-date",
            "date": "invalid-date-format", 
            "tags": [self.tag.id]
        }

        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors) 
