"""
Module for Category Model Tests.
This module will test all category model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.test import TestCase
from django.utils import timezone

from apps.blog.models import Category


class TesCategoryModel(TestCase):
    """
    Test User Model
    """

    def setUp(self) -> None:
        self._category_json = {
            "name": "Django",
            "description": "Python Web Framework",
            "updated_date": timezone.now(),
        }

    def test_category_creation(self):
        """
        Test Category Initialize
        """

        record = Category()
        self.assertIsInstance(record, Category)

    def test_category_creation_full(self):
        """
        Test Category full Initialize
        """

        record = Category.objects.create(**self._category_json)
        self.assertIsInstance(record, Category)

    def test_category_creation_full_verbose(self):
        """
        Test Category full Initialize verbose.
        """

        record = Category.objects.create(**self._category_json)
        self.assertIsInstance(record, Category)
        self.assertEqual(record.name, "Django")
        self.assertEqual(record.description, "Python Web Framework")

    def test_category_creation_set_values(self):
        """
        Test User Initialize with set values.
        """

        record = Category()
        record.set_values(pairs=self._category_json)
        record.save()

        self.assertIsInstance(record, Category)
        self.assertEqual(record.name, "Django")
        self.assertEqual(record.description, "Python Web Framework")
        self.assertEqual(record.slug, "django")

    def test_category_str(self):
        """
        Test Category str
        """

        record = Category.objects.create(**self._category_json)
        self.assertEqual(str(record), "Django")
