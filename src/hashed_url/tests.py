import unittest
import datetime

from hashed_url import utilities

from django.conf import settings

class TestUtilities(unittest.TestCase):
    
    def setUp(self):
        self.url = "https://moo.com:88/mooo/cow/?xx=yy&aa=bb"
        self._old_secret = settings.SECRET_KEY
        settings.SECRET_KEY = "mysecret"
    
    def tearDown(self):
        self.url = "https://moo.com:88/mooo/cow/?xx=yy&aa=bb"
        settings.SECRET_KEY = self._old_secret
    
    def test_append_param(self):
        self.assertEqual(utilities.append_param(self.url, "foo", "bar"), "https://moo.com:88/mooo/cow/?xx=yy&aa=bb&foo=bar")
    
    def test_remove_params(self):
        self.assertEqual(utilities.remove_params(self.url, ["xx", "aa", "moo"]), "https://moo.com:88/mooo/cow/")
    
    def test_get_hash_no_time(self):
        self.assertEqual(utilities.get_hash(self.url), "47f37d04c98a06a0c45790e0af2a1fd64129dfb2")
    
    def test_get_hash_with_time(self):
        t = 123 # fake timestamp
        self.assertEqual(utilities.get_hash(self.url, t), "839201dc174753d0099e3669a5841b94ddecb393")
    
    def test_get_hashed_url_no_time(self):
        url = utilities.get_hashed_url(self.url)
        expected = "https://moo.com:88/mooo/cow/?xx=yy&aa=bb&_t=&_h=47f37d04c98a06a0c45790e0af2a1fd64129dfb2"
        self.assertEqual(url, expected)
    
    def test_get_hashed_url_with_time(self):
        url = utilities.get_hashed_url(self.url, 123)
        expected = "https://moo.com:88/mooo/cow/?xx=yy&aa=bb&_t=123&_h=839201dc174753d0099e3669a5841b94ddecb393"
        self.assertEqual(url, expected)
    
    def test_get_hashed_url_with_datetime(self):
        url = utilities.get_hashed_url(self.url, datetime.datetime(2011, 6, 1, 9, 33, 22, 441717))
        expected = "https://moo.com:88/mooo/cow/?xx=yy&aa=bb&_t=1306920802&_h=effefe2db031944bee6b79943db24badf7f968fe"
        self.assertEqual(url, expected)
    
    def test_is_valid_url_ok(self):
        url = utilities.get_hashed_url(self.url, datetime.datetime.now() + datetime.timedelta(days=10))
        self.assertTrue(utilities.is_valid_url(url))
    
    def test_is_valid_url_expired(self):
        url = utilities.get_hashed_url(self.url, datetime.datetime.now() + datetime.timedelta(days=-10))
        self.assertFalse(utilities.is_valid_url(url))
    
    def test_is_valid_url_no_time(self):
        url = utilities.get_hashed_url(self.url)
        self.assertFalse(utilities.is_valid_url(url))
    
    def test_is_valid_url_no_hash(self):
        self.assertFalse(utilities.is_valid_url(self.url))
    
    def test_is_valid_url_bad_hash(self):
        url = utilities.get_hashed_url(self.url, datetime.datetime.now() + datetime.timedelta(days=10))
        url += "xxx"
        self.assertFalse(utilities.is_valid_url(url))
        

if __name__ == '__main__':
    unittest.main()