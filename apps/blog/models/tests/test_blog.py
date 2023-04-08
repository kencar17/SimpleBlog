"""
Module for Category Model Tests.
This module will test all category model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.account.models import Account, User
from apps.blog.models import BlogPost


class TesBlogPostModel(TestCase):
    """
    Test BlogPost Model
    """

    fixtures = ["tests/account.json"]

    def setUp(self) -> None:
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
            "account": self.account,
            "author": self.user,
            "status": "DRAFT",
            "title": "Exploring the Rich Culture of the Inuvialuit People",
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "content": "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        }

    def test_blog_creation(self):
        """
        Test BlogPost Initialize
        """

        record = BlogPost()
        self.assertIsInstance(record, BlogPost)

    def test_blog_creation_full(self):
        """
        Test BlogPost full Initialize
        """

        record = BlogPost.objects.create(**self._blog_json)
        self.assertIsInstance(record, BlogPost)

    def test_blog_creation_full_verbose(self):
        """
        Test BlogPost full Initialize verbose.
        """

        record = BlogPost.objects.create(**self._blog_json)
        record.account = self.account
        record.author = self.user
        self.assertIsInstance(record, BlogPost)
        self.assertEqual(record.status, "DRAFT")
        self.assertEqual(
            record.title, "Exploring the Rich Culture of the Inuvialuit People"
        )
        self.assertEqual(
            record.slug, "exploring-the-rich-culture-of-the-inuvialuit-people"
        )
        self.assertEqual(
            record.excerpt,
            "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
        )
        self.assertEqual(
            record.content,
            "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        )

    def test_blog_creation_set_values(self):
        """
        Test BlogPost Initialize with set values.
        """

        record = BlogPost()
        record.set_values(pairs=self._blog_json)
        record.account = self.account
        record.author = self.user
        record.save()

        self.assertIsInstance(record, BlogPost)
        self.assertEqual(record.status, "DRAFT")
        self.assertEqual(
            record.title, "Exploring the Rich Culture of the Inuvialuit People"
        )
        self.assertEqual(
            record.slug, "exploring-the-rich-culture-of-the-inuvialuit-people"
        )
        self.assertEqual(
            record.excerpt,
            "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
        )
        self.assertEqual(
            record.content,
            "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        )

    def test_blog_str(self):
        """
        Test BlogPost str
        """

        record = BlogPost.objects.create(**self._blog_json)
        record.account = self.account
        record.author = self.user
        self.assertEqual(
            str(record),
            "New Star Blog - Kenh Carml: Exploring the Rich Culture of the Inuvialuit People",
        )
