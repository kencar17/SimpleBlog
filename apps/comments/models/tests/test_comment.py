"""
Module for Comment Model Tests.
This module will test all comment model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.account.models import User
from apps.blog.models import BlogPost
from apps.comments.models import Comment


class TestCommentModel(TestCase):
    """
    Test BlogPost Model
    """

    fixtures = ["tests/account.json", "tests/user.json", "tests/blog.json"]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.blog = BlogPost.objects.first()

        self._comment_json = {
            "blog": self.blog,
            "author": self.user,
            "content": "Exploring the Rich Culture of the Inuvialuit People",
        }

    def test_comment_creation(self):
        """
        Test Comment Initialize
        """

        record = Comment()
        self.assertIsInstance(record, Comment)

    def test_comment_creation_full(self):
        """
        Test Comment full Initialize
        """

        record = Comment.objects.create(**self._comment_json)
        self.assertIsInstance(record, Comment)

    def test_comment_creation_full_verbose(self):
        """
        Test Comment full Initialize verbose.
        """

        record = Comment.objects.create(**self._comment_json)
        record.blog = self.blog
        record.author = self.user

        self.assertIsInstance(record, Comment)
        self.assertEqual(record.blog, self.blog)
        self.assertEqual(record.author, self.user)
        self.assertEqual(record.blog, self.blog)
        self.assertEqual(
            record.content, "Exploring the Rich Culture of the Inuvialuit People"
        )

    def test_comment_creation_set_values(self):
        """
        Test Comment Initialize with set values.
        """

        record = Comment()
        record.set_values(pairs=self._comment_json)
        record.blog = self.blog
        record.author = self.user
        record.save()

        self.assertIsInstance(record, Comment)
        self.assertEqual(record.blog, self.blog)
        self.assertEqual(record.author, self.user)
        self.assertEqual(record.blog, self.blog)
        self.assertEqual(
            record.content, "Exploring the Rich Culture of the Inuvialuit People"
        )

    def test_comment_str(self):
        """
        Test Comment str
        """

        record = Comment.objects.create(**self._comment_json)
        record.blog = self.blog
        record.author = self.user
        self.assertEqual(
            str(record),
            "New Star Blog - Kenneth Carmichael: Exploring the Rich Culture of the Inuvialuit People - K4 C4: Exploring the Rich Culture of the Inuvialuit People",
        )
