"""
Module for User Serializer Tests.
This module will test all user serializers methods and creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.account.validators.user_validators import (
    UppercaseValidator,
    SpecialCharValidator,
)


class TestUserValidators(TestCase):
    """
    Test User Serializer Model
    """

    def test_uppercase_validator(self):
        """
        Test User Validation uppercase
        """

        ret = UppercaseValidator().validate(password="K3nC@rIs!@wesom3!Too")
        self.assertIsNone(ret)

    def test_uppercase_validator_validation_error(self):
        """
        Test User Validation error no uppercase
        """

        with self.assertRaises(ValidationError) as e:
            ret = UppercaseValidator().validate(password="passwordonetwo")

        self.assertEqual(
            e.exception.message,
            "The password must contain at least 4 uppercase letter, A-Z.",
        )

    def test_uppercase_validator_validation_error_not_enough(self):
        """
        Test User Validation error not enough uppercase chars
        """

        with self.assertRaises(ValidationError) as e:
            ret = UppercaseValidator().validate(password="passwordonetwO")

        self.assertEqual(
            e.exception.message,
            "The password must contain at least 4 uppercase letter, A-Z.",
        )

    def test_uppercase_validator_get_help_text(self):
        """
        Test User Validation uppercase get help test
        """

        ret = UppercaseValidator().get_help_text()
        self.assertEqual(
            ret, "Your password must contain at least 4 uppercase letter, A-Z."
        )

    def test_special_char_validator(self):
        """
        Test User Validation special chars
        """

        ret = SpecialCharValidator().validate(password="K3nC@rIs!@wesom3!Too")
        self.assertIsNone(ret)

    def test_special_char_validator_validation_error(self):
        """
        Test User Validation error no special chars
        """

        with self.assertRaises(ValidationError) as e:
            ret = SpecialCharValidator().validate(password="passwordonetwo")

        self.assertEqual(
            e.exception.message,
            "The password must contain at least 4 special character: !@#$%^&*;:",
        )

    def test_special_char_validator_validation_error_not_enough(self):
        """
        Test User Validation error no special chars
        """

        with self.assertRaises(ValidationError) as e:
            ret = SpecialCharValidator().validate(password="passwordonetwo!")

        self.assertEqual(
            e.exception.message,
            "The password must contain at least 4 special character: !@#$%^&*;:",
        )

    def test_special_char_validator_get_help_text(self):
        """
        Test User Validation special_char get help test
        """

        ret = SpecialCharValidator().get_help_text()
        self.assertEqual(
            ret, "Your password must contain at least 4 special character: !@#$%^&*;:"
        )
