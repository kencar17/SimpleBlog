"""
Module for User Model Tests.
This module will test all user model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.account.models import User, Account


class TestUserModel(TestCase):
    """
    Test User Model
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

    def test_user_creation(self):
        """
        Test User Initialize
        """

        record = User()
        self.assertIsInstance(record, User)

    def test_user_creation_full(self):
        """
        Test User full Initialize
        """

        record = User.objects.create(**self._user_json)
        self.assertIsInstance(record, User)

    def test_user_creation_full_verbose(self):
        """
        Test User full Initialize verbose.
        """

        record = User.objects.create(**self._user_json)
        self.assertIsInstance(record, User)
        self.assertEqual(record.username, "ken3@kencar.ca")
        self.assertEqual(record.email, "ken3@kencar.ca")
        self.assertEqual(record.first_name, "Kenh")
        self.assertEqual(record.last_name, "Carml")
        self.assertEqual(record.bio, "Personal Blog of Kenneth Carmichael")
        self.assertTrue(record.is_contributor)
        self.assertTrue(record.is_editor)
        self.assertFalse(record.is_blog_owner)
        self.assertTrue(record.is_active)
        self.assertFalse(record.is_staff)
        self.assertFalse(record.is_superuser)

    def test_user_creation_set_values(self):
        """
        Test User Initialize with set values.
        """

        record = User()
        record.set_values(pairs=self._user_json)
        record.account = self.account
        record.save()

        self.assertIsInstance(record, User)
        self.assertEqual(record.username, "ken3@kencar.ca")
        self.assertEqual(record.email, "ken3@kencar.ca")
        self.assertEqual(record.first_name, "Kenh")
        self.assertEqual(record.last_name, "Carml")
        self.assertEqual(record.bio, "Personal Blog of Kenneth Carmichael")
        self.assertTrue(record.is_contributor)
        self.assertTrue(record.is_editor)
        self.assertFalse(record.is_blog_owner)
        self.assertTrue(record.is_active)
        self.assertFalse(record.is_staff)
        self.assertFalse(record.is_superuser)

    def test_user_str(self):
        """
        Test User str
        """

        record = User.objects.create(**self._user_json)
        self.assertEqual(str(record), "Kenh Carml")
