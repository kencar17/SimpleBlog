"""
Module for Tag Model Tests.
This module will test all tag model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.test import TestCase
from django.utils import timezone

from apps.blog.models import Tag


class TestTagModel(TestCase):
    """
    Test Tag Model
    """

    def setUp(self) -> None:
        self._tag_json = {
            "name": "Python",
            "description": "Python Language",
            "updated_date": timezone.now(),
        }

    def test_tag_creation(self):
        """
        Test Tag Initialize
        """

        record = Tag()
        self.assertIsInstance(record, Tag)

    def test_tag_creation_full(self):
        """
        Test Tag full Initialize
        """

        record = Tag.objects.create(**self._tag_json)
        self.assertIsInstance(record, Tag)

    def test_tag_creation_full_verbose(self):
        """
        Test Tag full Initialize verbose.
        """

        record = Tag.objects.create(**self._tag_json)
        self.assertIsInstance(record, Tag)
        self.assertEqual(record.name, "Python")
        self.assertEqual(record.description, "Python Language")

    def test_tag_creation_set_values(self):
        """
        Test Tag Initialize with set values.
        """

        record = Tag()
        record.set_values(pairs=self._tag_json)
        record.save()

        self.assertIsInstance(record, Tag)
        self.assertEqual(record.name, "Python")
        self.assertEqual(record.description, "Python Language")
        self.assertEqual(record.slug, "python")

    def test_tag_str(self):
        """
        Test Tag str
        """

        record = Tag.objects.create(**self._tag_json)
        self.assertEqual(str(record), "Python")
