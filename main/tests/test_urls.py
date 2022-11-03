from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import login_view, register_view, logout_view, index_view

class TestUrls(SimpleTestCase):
    """
    This class tests if views are bound to urls correctly.
    """

    def test_login_url(self):
        
        url = reverse('login')

        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url(self):

        url = reverse('logout')

        self.assertEquals(resolve(url).func, logout_view)
    
    def test_register_url(self):

        url = reverse('sign-up')

        self.assertEquals(resolve(url).func, register_view)
    
    def test_index_url(self):

        url = reverse('index')

        self.assertEquals(resolve(url).func, index_view)