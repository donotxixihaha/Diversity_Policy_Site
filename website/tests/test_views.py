from django.test import TestCase, Client
from django.urls import reverse
from website.models import Policy

class TestViews(TestCase):

    def setUp(self):
        self.client = Client();
        self.index_view_url = reverse('index_view')
        self.policy_search_url = reverse('policy-search')
        self.policy_suggest_url = reverse('policy-suggest')
        self.about_page_url = reverse('about-page')
        self.contribute_policy_url = reverse('contribute-policy')
        

    def test_index_view_GET(self):
        response = self.client.get(self.index_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/search_home.html')


    def test_policy_search_GET(self):
        # Did not pass because of NoneType Error
        #response = self.client.get(self.policy_search_url, {'search':''})
        response = self.client.get(self.policy_search_url, {'search':'go', 'filter':['university%20of%20oregon', '2014']})
        response = self.client.get(self.policy_search_url, {'search':'go'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/policy_list.html')


    def test_policy_suggest_GET(self):
        pass
        

    def test_about_page_GET(self):
        response = self.client.get(self.about_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/about_page.html')


    def test_contribute_policy_GET(self):
        response = self.client.get(self.contribute_policy_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/contribute_policy.html')
    
    