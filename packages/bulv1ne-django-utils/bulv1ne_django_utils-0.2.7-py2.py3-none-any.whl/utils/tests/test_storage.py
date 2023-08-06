from datetime import datetime
from unittest.mock import MagicMock

from django.core.cache import cache
from django.test import TestCase, override_settings
from utils.storage import S3HeadCacheMixin

s3client = MagicMock()
s3client.head_object = MagicMock(
    return_value={"ContentLength": 123, "LastModified": datetime(2015, 1, 1)}
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}


class MockS3Storage(S3HeadCacheMixin):
    def __init__(self):
        self.s3client = s3client
        self.bucket = "s3-bucket"


@override_settings(CACHES=CACHES)
class StorageTestCase(TestCase):
    def setUp(self):
        self.storage = MockS3Storage()

    def tearDown(self):
        cache.clear()

    def test_cache_save(self):
        data = self.storage.get_head("my_file.txt")
        cache_data = cache.get(self.storage.get_cache_key("my_file.txt"))
        self.assertEqual(cache_data, data)

    def test_reset_head(self):
        self.storage.reset_head("my_file.txt")
        cache_data = cache.get(self.storage.get_cache_key("my_file.txt"))
        self.assertIsNone(cache_data)

    def test_MemcachedKeyCharacterError(self):
        filename = "dir/to/file/weird file with åäö.txt"
        data = self.storage.get_head(filename)
        cache_data = cache.get(self.storage.get_cache_key(filename))
        self.assertEqual(cache_data, data)
