from django.test import TestCase, Client
from django.urls import reverse
from website.models import Policy

class TestViews(TestCase):

    def setUp(self):
        self.client = Client();
        self.index_view_url = reverse('index_view')

    def test_index_view_GET(self):
        response = self.client.get(self.index_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/search_home.html')