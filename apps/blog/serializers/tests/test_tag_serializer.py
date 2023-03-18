"""
Module for Tag Serializer Tests.
This module will test all tag serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 4th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.blog.models import Tag
from apps.blog.serializers.tag_serializer import CreateTagSerializer, TagSerializer


class TestTagSerializerModel(TestCase):
    """
    Test Tag Serializer Model
    """

    def setUp(self) -> None:
        self._tag_json = {
            "name": "Javascript",
            "description": "Programming Language",
        }

    def test_tag_serializer_creation(self):
        """
        Test Tag Initialize
        """

        serializer = CreateTagSerializer(data=self._tag_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, Tag)
        self.assertEqual(instance.name, "Javascript")
        self.assertEqual(instance.description, "Programming Language")
        self.assertEqual(instance.slug, "javascript")

    def test_tag_serializer_list(self):
        """
        Test Tag Initialize
        """

        serializer = CreateTagSerializer(data=self._tag_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        ret = TagSerializer(instance, many=False).data
        expected = {
            "name": "Javascript",
            "description": "Programming Language",
            "slug": "javascript",
        }
        del ret["id"]
        del ret["created_date"]
        del ret["updated_date"]

        self.assertIsInstance(ret, dict)
        self.assertDictEqual(ret, expected)
