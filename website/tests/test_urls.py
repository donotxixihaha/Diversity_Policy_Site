from django.test import SimpleTestCase
from django.urls import reverse, resolve
from website.views import search_home, policy_search, autocompleteModel, about_page, contribute_policy
class TestUrls(SimpleTestCase):

    def test_index_view_url_resolves(self):
        url = reverse('index_view')
        self.assertEquals(resolve(url).func, search_home)
    
    def test_policy_search_url_resolves(self):
        url = reverse('policy-search')
        self.assertEquals(resolve(url).func, policy_search)

    def test_policy_suggest_url_resolves(self):
        url = reverse('policy-suggest')
        self.assertEquals(resolve(url).func, autocompleteModel)

    def test_about_page_url_resolves(self):
        url = reverse('about-page')
        self.assertEquals(resolve(url).func, about_page)

    def test_contribute_policy_url_resolves(self):
        url = reverse('contribute-policy')
        self.assertEquals(resolve(url).func, contribute_policy)