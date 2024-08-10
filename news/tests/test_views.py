from ..models import Tag, News
from ..serializers import TagSerializer, NewsSerializer
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

# Tests for views.py
class TagViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(tag_label="T1(g)ی")

    def test_list_tags(self):
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tag_label'], "T1(g)ی")

    def test_retrieve_tag(self):
        tag = self.client.get(reverse('tag-detail', args=[self.tag.id]))
        self.assertEqual(tag.status_code, 200)
        self.assertEqual(tag.data['tag_label'], "T1(g)ی")


class NewsViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(tag_label="N3(w)ی")
        self.filter_tag = Tag.objects.create(tag_label="filter-tag")

        self.news = News.objects.create(
            title="N3(w)ی",
            text="Th!s is @noth3r f@ke new$.",
            resource="http://example.com/fake"
        )

        self.filter_news1 = News.objects.create(
            title="filter news 1",
            text="filter news for testing filtering.",
            resource="http://filter1.com/"
        )

        self.filter_news2 = News.objects.create(
            title="filter news 2",
            text="filter news for testing filtering.",
            resource="http://filter2.com/"
        )

        self.news.tags.add(self.tag)
        self.filter_news1.tags.add(self.filter_tag)
        self.filter_news2.tags.add(self.filter_tag)

    def test_list_news(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], "N3(w)ی")
        self.assertEqual(response.data['results'][1]['title'], "filter news 1")
        self.assertEqual(response.data['results'][2]['title'], "filter news 2")

    def test_filter_news_by_tag(self):
        response = self.client.get(reverse('news-list'), {'tags': self.filter_tag.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], "filter news 1")
        self.assertEqual(response.data['results'][1]['title'], "filter news 2")
        self.assertNotIn("N3(w)ی", [news['title'] for news in response.data['results']])

    def test_retrieve_news(self):
        response = self.client.get(reverse('news-detail', args=[self.news.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "N3(w)ی")
