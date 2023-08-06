import os
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class PipelineTestCase(TestCase):
    def setUp(self):
        self.file_path = os.path.join(settings.STATIC_ROOT, "staticfiles.json")
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    def test_success(self):
        call_command("collectstatic", "--noinput", stdout=StringIO())
        call_command("clean_staticfilesjson", stdout=StringIO())
        with open(self.file_path) as f:
            contents = f.read()
            start_content = '{\n    "paths": {\n'
            self.assertTrue(
                contents.startswith(start_content),
                'staticfiles.json doesn\'t start with "{}"'.format(
                    contents[: len(start_content)]
                ),
            )

    def test_missing_staticfilesjson(self):
        with self.assertRaises(CommandError):
            call_command("clean_staticfilesjson", stdout=StringIO())
