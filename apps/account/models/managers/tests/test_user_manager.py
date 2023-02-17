"""
Module for User Manager Tests.
This module will test all user model methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""
from django.db.models import QuerySet
from django.test import TestCase

from apps.account.models import User, Account


class TestUserManager(TestCase):
    """
        Test User Model
    """

    fixtures = [
        "tests/account.json"
    ]

    def setUp(self) -> None:
        self.account = Account.objects.first()

    def test_user_create(self):
        """
        Test User manager create.
        """

        record = User.objects.create_user(username="email@email.com", password="MyPassword1234!", account=self.account)

        self.assertIsInstance(record, User)
        self.assertEqual(record.username, "email@email.com")

    def test_user_create_empty_username(self):
        """
        Test User manager create empty username error.
        """

        with self.assertRaises(ValueError) as e:

            record = User.objects.create_user(username="", password="MyPassword1234!", account=self.account)

        self.assertEqual(str(e.exception), "The given username must be set")

    def test_user_create_superuser(self):
        """
        Test User manager create superuser.
        """

        record = User.objects.create_superuser(
            username="email@email.com",
            password="MyPassword1234!",
            account=self.account
        )

        self.assertIsInstance(record, User)
        self.assertEqual(record.username, "email@email.com")

    def test_user_create_superuser_is_staff_false(self):
        """
        Test User manager create superuser.
        """

        with self.assertRaises(ValueError) as e:
            record = User.objects.create_superuser(
                username="email@email.com",
                password="MyPassword1234!",
                account=self.account,
                is_staff=False
            )

        self.assertEqual(str(e.exception), "Superuser must have is_staff=True.")

    def test_user_create_superuser_is_superuser_false(self):
        """
        Test User manager create superuser.
        """

        with self.assertRaises(ValueError) as e:
            record = User.objects.create_superuser(
                username="email@email.com",
                password="MyPassword1234!",
                account=self.account,
                is_superuser=False
            )

        self.assertEqual(str(e.exception), "Superuser must have is_superuser=True.")

    def test_user_contributors(self):
        """
        Test User manager contributors QuerySet.
        """

        record = User.objects.contributors()

        self.assertIsInstance(record, QuerySet)

    def test_user_editors(self):
        """
        Test User manager editors QuerySet.
        """

        record = User.objects.editors()

        self.assertIsInstance(record, QuerySet)

    def test_user_blog_owners(self):
        """
        Test User manager blog_owners QuerySet.
        """

        record = User.objects.blog_owners()

        self.assertIsInstance(record, QuerySet)
