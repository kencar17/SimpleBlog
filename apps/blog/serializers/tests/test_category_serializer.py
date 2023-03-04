"""
Module for Category Serializer Tests.
This module will test all category serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.test import TestCase

from apps.blog.models import Category
from apps.blog.serializers.category_serializer import (
    CreateCategorySerializer,
    CategorySerializer,
)


class TestCategorySerializerModel(TestCase):
    """
    Test Category Serializer Model
    """

    def setUp(self) -> None:
        self._category_json = {
            "name": "Portfolio",
            "description": "Personal Portfolio",
        }

    def test_category_serializer_creation(self):
        """
        Test Category Initialize
        """

        serializer = CreateCategorySerializer(data=self._category_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, Category)
        self.assertEqual(instance.name, "Portfolio")
        self.assertEqual(instance.description, "Personal Portfolio")
        self.assertEqual(instance.slug, "portfolio")

    def test_category_serializer_list(self):
        """
        Test Category Initialize
        """

        serializer = CreateCategorySerializer(data=self._category_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        ret = CategorySerializer(instance, many=False).data
        expected = {
            "name": "Portfolio",
            "description": "Personal Portfolio",
            "slug": "portfolio",
            "parent": None,
        }
        del ret["id"]
        del ret["created_date"]
        del ret["updated_date"]

        self.assertIsInstance(ret, dict)
        self.assertDictEqual(ret, expected)
