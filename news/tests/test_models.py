from ..models import Tag, News
from django.test import TestCase
from django.db import IntegrityError

# tests for models.py
class TagModelTest(TestCase):

    def test_tag_string_representation(self):
        tag = Tag.objects.create(tag_label="!t@g&^0تگ tag")
        self.assertEqual(str(tag), "!t@g&^0تگ tag")

    def test_deleting_tag_removes_relationship(self):
        tag = Tag.objects.create(tag_label="!t@g&^0تگ tag")
        news = News.objects.create(
            title="Br#*ng خبر!",
            text="This is a fake news for تست.٪×",
            resource="http://fakenews3.com/"
        )
        news.tags.add(tag)
        tag.delete()
        self.assertNotIn(tag, news.tags.all())

    def test_tag_label_max_length(self):
        tag = Tag.objects.create(tag_label="A" * 50)
        self.assertEqual(len(tag.tag_label), 50)
        
    def test_duplicate_tags(self):
        Tag.objects.create(tag_label="DuplicateTag")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(tag_label="DuplicateTag")


class NewsModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(tag_label="T1(g)ی")
        self.news = News.objects.create(
            title="Br#*ng خبر!",
            text="This is a fake news for تست.٪×",
            resource="http://fakenews3.com/"
        )
        self.news.tags.add(self.tag)

    def test_string_representation(self):
        self.assertEqual(str(self.news), "Br#*ng خبر!")

    def test_news_has_tags(self):
        self.assertIn(self.tag, self.news.tags.all())

    def test_deleting_news_cascades_properly(self):
        news_id = self.news.id
        self.news.delete()
        self.assertFalse(News.objects.filter(id=news_id).exists())
    
    def test_news_resource_unique_constraint(self):
        with self.assertRaises(Exception):
            News.objects.create(
                title="Duplicate resource",
                text="Trying to create news with duplicate resource",
                resource="http://fakenews3.com/"
            )

    def test_news_title_max_length(self):
        news = News.objects.create(
            title="A" * 255,
            text="Testing max length of title.",
            resource="http://fakenews5.com/"
        )
        self.assertEqual(len(news.title), 255)

    def test_news_duplicate_titles(self):
        with self.assertRaises(IntegrityError):
            News.objects.create(
                title="Br#*ng خبر!",
                text="Testing duplicate title.",
                resource="http://fakenews5.com/"
            )