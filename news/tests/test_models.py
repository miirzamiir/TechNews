from ..models import Tag, News
from django.test import TestCase

# tests for models.py
class TagModelTest(TestCase):

    def test_tag_string_representation(self):
        tag = Tag.objects.create(tag_label="!t@g&^0تگ tag")
        self.assertEqual(str(tag), "!t@g&^0تگ tag")

    def test_deleting_tag_removes_relationship(self):
        self.tag = Tag.objects.create(tag_label="!t@g&^0تگ tag")
        self.news = News.objects.create(
            title="Br#*ng خبر!",
            text="This is a fake news for تست.٪×",
            resource="http://fakenews3.com/"
        )

        self.tag.delete()
        self.assertNotIn(self.tag, self.news.tags.all())


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
        