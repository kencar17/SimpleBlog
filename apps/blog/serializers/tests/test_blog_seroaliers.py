"""
Module for Blog Post Serializer Tests.
This module will test all blog post serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""
from uuid import UUID

from django.test import TestCase

from apps.account.models import Account, User
from apps.blog.models import BlogPost
from apps.blog.serializers.blog_serializers import (
    CreateBlogPostSerializer,
    BlogPostExcerptSerializer,
    BlogPostSerializer,
)


class TestBlogPostSerializerModel(TestCase):
    """
    Test Blog Post Serializer Model
    """

    fixtures = ["tests/account.json"]

    def setUp(self) -> None:
        self.maxDiff = None
        self.account = Account.objects.first()

        self._user_json = {
            "account": self.account,
            "username": "ken3@kencar.ca",
            "email": "ken3@kencar.ca",
            "display_name": "",
            "first_name": "Kenh",
            "last_name": "Carml",
            "bio": "Personal Blog of Kenneth Carmichael",
            "is_contributor": True,
            "is_editor": True,
            "is_blog_owner": False,
            "password": "AmATestPasswordToday",
        }
        self.user = User.objects.create(**self._user_json)
        self.user.save()

        self._blog_json = {
            "account": str(self.account.id),
            "author": str(self.user.id),
            "status": "DRAFT",
            "title": "Exploring the Rich Culture of the Inuvialuit People",
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "content": "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        }

    def test_blog_serializer_creation(self):
        """
        Test Blog Post Initialize
        """

        serializer = CreateBlogPostSerializer(data=self._blog_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, BlogPost)
        self.assertEqual(instance.status, "DRAFT")
        self.assertEqual(
            instance.title, "Exploring the Rich Culture of the Inuvialuit People"
        )
        self.assertEqual(
            instance.slug, "exploring-the-rich-culture-of-the-inuvialuit-people"
        )
        self.assertEqual(
            instance.excerpt,
            "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
        )
        self.assertEqual(
            instance.content,
            "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        )

    def test_blog_excerpt_serializer_list(self):
        """
        Test Blog Post Initialize
        """

        serializer = CreateBlogPostSerializer(data=self._blog_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        ret = BlogPostExcerptSerializer(instance, many=False).data
        expected = {
            "account": UUID("5b076883-8f47-4372-9089-7f2a9e68f69f"),
            "published_date": None,
            "status": "DRAFT",
            "views": 0,
            "likes": 0,
            "dislikes": 0,
            "title": "Exploring the Rich Culture of the Inuvialuit People",
            "slug": "exploring-the-rich-culture-of-the-inuvialuit-people",
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "categories": [],
            "tags": [],
            "is_featured": False,
        }

        del ret["id"]
        del ret["created_date"]
        del ret["updated_date"]
        del ret["author"]

        self.assertIsInstance(ret, dict)
        self.assertDictEqual(ret, expected)

    def test_blog_serializer_list(self):
        """
        Test Blog Post Initialize
        """

        serializer = CreateBlogPostSerializer(data=self._blog_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        ret = BlogPostSerializer(instance, many=False).data
        expected = {
            "account": UUID("5b076883-8f47-4372-9089-7f2a9e68f69f"),
            "published_date": None,
            "status": "DRAFT",
            "views": 0,
            "likes": 0,
            "dislikes": 0,
            "title": "Exploring the Rich Culture of the Inuvialuit People",
            "slug": "exploring-the-rich-culture-of-the-inuvialuit-people",
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "categories": [],
            "tags": [],
            "is_featured": False,
            "content": "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        }

        del ret["id"]
        del ret["created_date"]
        del ret["updated_date"]
        del ret["author"]

        self.assertIsInstance(ret, dict)
        self.assertDictEqual(ret, expected)
