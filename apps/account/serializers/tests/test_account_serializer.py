"""
Module for Account Serializer Tests.
This module will test all account serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 28th 2023
Version: 1.0
"""
import copy

from django.test import TestCase
from rest_framework import serializers

from apps.account.models import Account, User
from apps.account.serializers.account_serializer import CreateAccountSerializer
from apps.account.serializers.user_serializer import (
    UserSerializer,
    CreateUserSerializer,
    UserChangePasswordSerializer,
)


class TestAccountSerializerModel(TestCase):
    """
    Test Account Serializer Model
    """

    fixtures = ["tests/account.json"]

    def setUp(self) -> None:
        self._account_json = {
            "account_name": "KENCAR",
            "bio": "Am a blog for mememememe",
            "contact_email": "kencar8@kencar.com",
        }

    def test_account_serializer_creation(self):
        """
        Test Account Initialize
        """

        serializer = CreateAccountSerializer(data=self._account_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, Account)
        self.assertEqual(instance.account_name, "KENCAR")
        self.assertEqual(instance.bio, "Am a blog for mememememe")
        self.assertEqual(instance.contact_email, "kencar8@kencar.com")

    def test_account_serializer_creation_empty_bio(self):
        """
        Test Account Initialize
        """
        copied = copy.deepcopy(self._account_json)
        copied["bio"] = ""

        serializer = CreateAccountSerializer(data=copied)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, Account)
        self.assertEqual(instance.account_name, "KENCAR")
        self.assertEqual(instance.bio, "Am a blog for KENCAR")
        self.assertEqual(instance.contact_email, "kencar8@kencar.com")
