"""
Module for Comment Serializer Tests.
This module will test all comment serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""
from uuid import UUID

from django.test import TestCase

from apps.account.models import User
from apps.blog.models import BlogPost
from apps.comments.models import Comment
from apps.comments.serializers.comment_serializers import (
    CreateCommentSerializer,
    CommentSerializer,
)


class TestCommentSerializerModel(TestCase):
    """
    Test Comment Serializer Model
    """

    fixtures = ["tests/account.json", "tests/user.json", "tests/blog.json"]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.blog = BlogPost.objects.first()

        self._comment_json = {
            "blog": str(self.blog.id),
            "author": str(self.user.id),
            "content": "Exploring the Rich Culture of the Inuvialuit People",
        }

    def test_comment_serializer_creation(self):
        """
        Test Comment Initialize
        """

        serializer = CreateCommentSerializer(data=self._comment_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, Comment)
        self.assertIsInstance(instance.blog, BlogPost)
        self.assertIsInstance(instance.author, User)
        self.assertEqual(
            instance.content, "Exploring the Rich Culture of the Inuvialuit People"
        )

    def test_comment_serializer_list(self):
        """
        Test Comment Initialize
        """

        serializer = CreateCommentSerializer(data=self._comment_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        ret = CommentSerializer(instance, many=False).data
        expected = {
            "blog": UUID("335ce286-c177-4f9a-af25-05c3a94975fb"),
            "author": UUID("10c331ef-d067-488e-8c0f-e398d7c8d9d3"),
            "parent": None,
            "content": "Exploring the Rich Culture of the Inuvialuit People",
            "children": [],
        }
        del ret["id"]
        del ret["created_date"]

        self.assertIsInstance(ret, dict)
        self.assertDictEqual(ret, expected)
