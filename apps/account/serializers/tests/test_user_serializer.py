"""
Module for User Serializer Tests.
This module will test all user serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""
import copy

from django.test import TestCase
from rest_framework import serializers

from apps.account.models import Account, User
from apps.account.serializers.user_serializer import (
    UserSerializer,
    CreateUserSerializer,
    UserChangePasswordSerializer,
)


class TestUserSerializerModel(TestCase):
    """
    Test User Serializer Model
    """

    fixtures = ["tests/account.json"]

    def setUp(self) -> None:
        self.account = Account.objects.first()

        self._user_json = {
            "account": str(self.account.id),
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

        self._update_json = {
            "display_name": "email",
            "first_name": "email",
            "last_name": "email",
            "bio": "Carmichael",
        }

    def test_user_serializer_creation(self):
        """
        Test User Initialize
        """

        serializer = CreateUserSerializer(data=self._user_json)

        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)

        self.assertIsInstance(instance, User)
        self.assertEqual(instance.username, "ken3@kencar.ca")
        self.assertEqual(instance.email, "ken3@kencar.ca")
        self.assertEqual(instance.first_name, "Kenh")
        self.assertEqual(instance.last_name, "Carml")
        self.assertEqual(instance.bio, "Personal Blog of Kenneth Carmichael")
        self.assertTrue(instance.is_contributor)
        self.assertTrue(instance.is_editor)
        self.assertFalse(instance.is_blog_owner)
        self.assertTrue(instance.is_active)
        self.assertFalse(instance.is_staff)
        self.assertFalse(instance.is_superuser)

    def test_user_serializer_update(self):
        """
        Test User Initialize
        """
        copied = copy.deepcopy(self._user_json)
        copied["account"] = self.account
        user = User.objects.create(**copied)
        user.save()

        serializer = UserSerializer(data=self._update_json, partial=True)
        serializer.is_valid()

        instance = serializer.update(
            instance=user, validated_data=serializer.validated_data
        )

        self.assertIsInstance(instance, User)
        self.assertEqual(instance.display_name, "email")
        self.assertEqual(instance.first_name, "email")
        self.assertEqual(instance.last_name, "email")
        self.assertEqual(instance.bio, "Carmichael")

    def test_user_serializer_password_change(self):
        """
        Test User Password Change Serializer
        """
        copied = copy.deepcopy(self._user_json)
        copied["account"] = self.account
        user = User.objects.create(**copied)
        user.save()

        data = {
            "password_one": "K3nC@rIs!@wesom3!Too",
            "password_two": "K3nC@rIs!@wesom3!Too",
        }

        serializer = UserChangePasswordSerializer(data=data)
        serializer.is_valid()

        instance = serializer.update(
            instance=user, validated_data=serializer.validated_data
        )

        self.assertIsInstance(instance, User)

    def test_user_serializer_password_change_error(self):
        """
        Test User Password Change Serializer
        """
        copied = copy.deepcopy(self._user_json)
        copied["account"] = self.account
        user = User.objects.create(**copied)
        user.save()

        data = {
            "password_one": "PASApasswordonetwo",
            "password_two": "PASApasswordonetwo",
        }

        serializer = UserChangePasswordSerializer(data=data)
        serializer.is_valid()

        with self.assertRaises(serializers.ValidationError) as e:
            instance = serializer.update(
                instance=user, validated_data=serializer.validated_data
            )

        expected = "{'password': [ErrorDetail(string='The password must contain at least 4 special character: !@#$%^&*;:', code='invalid')]}"

        self.assertEqual(str(e.exception.detail), expected)

    def test_user_serializer_password_change_not_the_same(self):
        """
        Test User Password Change Serializer
        """
        copied = copy.deepcopy(self._user_json)
        copied["account"] = self.account
        user = User.objects.create(**copied)
        user.save()

        data = {
            "password_one": "K3nC@rIs!@wesom3!Too",
            "password_two": "K3nC@rIs!@wesom3!Toocksdmldc",
        }

        serializer = UserChangePasswordSerializer(data=data)
        serializer.is_valid()

        with self.assertRaises(serializers.ValidationError) as e:
            instance = serializer.update(
                instance=user, validated_data=serializer.validated_data
            )

        expected = "{'password': [ErrorDetail(string='Passwords do not match', code='invalid')]}"

        self.assertEqual(str(e.exception.detail), expected)
