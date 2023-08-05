from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from .core import shorten_url, unshorten_url
from .models import UrlIndex




class ShortnrTestCase(TestCase):

    
    def setUp(self):
        self.url = 'http://www.google.com'
        self.shortnd_url = UrlIndex.objects.create(url=self.url)



    def test_method_shorten_url_returns_shortend_url_object_if_passed_url_does_not_exist(self):
        url = 'http://youtube.com'
        obj = shorten_url(url)
        self.assertEqual(obj.url, url)



    def test_method_shorten_url_returns_shortend_url_object_if_passed_url_exists(self):
        obj = shorten_url(self.url)
        self.assertEqual(obj.url, self.url)



    def test_method_unshorten_url_returns_shortend_url_object_if_passed_key_exists(self):
        obj = unshorten_url(self.shortnd_url.key)
        self.assertEqual(obj.key, self.shortnd_url.key)



    def test_method_unshorten_url_raises_error_if_key_doesnt_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            unshorten_url('notkey1')
