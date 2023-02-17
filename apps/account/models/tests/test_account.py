"""
Module for Account Model Tests.
This module will test all account model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.account.models import Account


class TestAccountModel(TestCase):
    """
    Test Account Model
    """

    fixtures = ["tests/account.json"]

    def setUp(self) -> None:
        self._account_json = {
            "account_name": "Test Account",
            "bio": "Am a blog",
            "contact_email": "email@email.com",
            "website_link": "https://www.kencar.com",
            "facebook_link": "https://www.kencar.com",
            "instagram_link": "https://www.kencar.com",
            "twitter_link": "https://www.kencar.com",
            "tiktok_link": "https://www.kencar.com",
            "linkedin_link": "https://www.kencar.com",
            "snapchat_link": "https://www.kencar.com",
            "youtube_link": "https://www.kencar.com",
            "twitch_link": "https://www.kencar.com",
        }

    def test_account_creation(self):
        """
        Test Account Initialize
        """

        record = Account()
        self.assertIsInstance(record, Account)

    def test_account_creation_full(self):
        """
        Test Account full Initialize
        """

        record = Account.objects.create(**self._account_json)
        self.assertIsInstance(record, Account)

    def test_account_creation_full_verbose(self):
        """
        Test account full Initialize verbose.
        """

        record = Account.objects.create(**self._account_json)
        self.assertIsInstance(record, Account)
        self.assertEqual(record.account_name, "Test Account")
        self.assertEqual(record.bio, "Am a blog")
        self.assertEqual(record.contact_email, "email@email.com")
        self.assertEqual(record.website_link, "https://www.kencar.com")
        self.assertEqual(record.facebook_link, "https://www.kencar.com")
        self.assertEqual(record.instagram_link, "https://www.kencar.com")
        self.assertEqual(record.twitter_link, "https://www.kencar.com")
        self.assertEqual(record.tiktok_link, "https://www.kencar.com")
        self.assertEqual(record.linkedin_link, "https://www.kencar.com")
        self.assertEqual(record.snapchat_link, "https://www.kencar.com")
        self.assertEqual(record.youtube_link, "https://www.kencar.com")
        self.assertEqual(record.twitch_link, "https://www.kencar.com")

    def test_account_creation_set_values(self):
        """
        Test account Initialize with set values.
        """

        record = Account()
        record.set_values(pairs=self._account_json)
        record.save()

        self.assertIsInstance(record, Account)
        self.assertEqual(record.account_name, "Test Account")
        self.assertEqual(record.bio, "Am a blog")
        self.assertEqual(record.contact_email, "email@email.com")
        self.assertEqual(record.website_link, "https://www.kencar.com")
        self.assertEqual(record.facebook_link, "https://www.kencar.com")
        self.assertEqual(record.instagram_link, "https://www.kencar.com")
        self.assertEqual(record.twitter_link, "https://www.kencar.com")
        self.assertEqual(record.tiktok_link, "https://www.kencar.com")
        self.assertEqual(record.linkedin_link, "https://www.kencar.com")
        self.assertEqual(record.snapchat_link, "https://www.kencar.com")
        self.assertEqual(record.youtube_link, "https://www.kencar.com")
        self.assertEqual(record.twitch_link, "https://www.kencar.com")

    def test_account_str(self):
        """
        Test account str
        """

        record = Account.objects.first()
        self.assertEqual(str(record), "New Star Blog")
