from ..models import Tag, News
from ..serializers import TagSerializer, NewsSerializer
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

# Tests for views.py
class TagViewSetTest(APITestCase):
    """
    TestCase for the TagViewSet. Contains unit tests to verify the functionality
    of the TagViewSet, including listing, retrieving, and filtering by tags.
    """

    def setUp(self):
        """Sets up initial test data, including a Tag instance and APIClient."""
        self.client = APIClient()
        self.tag = Tag.objects.create(tag_label="T1(g)ی")

    def test_list_tags(self):
        """Tests the listing of tags through the API."""
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tag_label'], "T1(g)ی")

    def test_retrieve_tag(self):
        """Tests the retrieval of a single tag via the API."""
        tag = self.client.get(reverse('tag-detail', args=[self.tag.id]))
        self.assertEqual(tag.status_code, 200)
        self.assertEqual(tag.data['tag_label'], "T1(g)ی")

    def test_search_tag(self):
        """Tests searching for tags via the API."""
        search_tag1 = Tag.objects.create(tag_label="search tag 1")
        search_tag2 = Tag.objects.create(tag_label="search tag 2")
        response = self.client.get(reverse('tag-list'), {'search': 'search'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['tag_label'], "search tag 1")
        self.assertEqual(response.data['results'][1]['tag_label'], "search tag 2")
        self.assertNotIn("T1(g)ی", [tags['tag_label'] for tags in response.data['results']])


class NewsViewSetTest(APITestCase):
    """
    TestCase for the NewsViewSet. Contains unit tests to verify the functionality
    of the NewsViewSet, including listing, filtering, searching, and retrieving news items.
    """

    def setUp(self):
        """Sets up initial test data, including Tag and News instances, and APIClient."""
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
        """Tests the listing of news items through the API."""
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], "N3(w)ی")
        self.assertEqual(response.data['results'][1]['title'], "filter news 1")
        self.assertEqual(response.data['results'][2]['title'], "filter news 2")

    def test_filter_news_by_tag(self):
        """Tests filtering news items by tag through the API."""
        response = self.client.get(reverse('news-list'), {'tags': self.filter_tag.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], "filter news 1")
        self.assertEqual(response.data['results'][1]['title'], "filter news 2")
        self.assertNotIn("N3(w)ی", [news['title'] for news in response.data['results']])

    def test_search_news(self):
        """Tests searching for news items through the API."""
        response = self.client.get(reverse('news-list'), {'search': 'news'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], "filter news 1")
        self.assertEqual(response.data['results'][1]['title'], "filter news 2")
        self.assertNotIn("N3(w)ی", [news['title'] for news in response.data['results']])

    def test_retrieve_news(self):
        """Tests the retrieval of a single news item through the API."""
        response = self.client.get(reverse('news-detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "N3(w)ی")
