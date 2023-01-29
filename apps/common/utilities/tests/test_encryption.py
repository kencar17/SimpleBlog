"""
Module for encryption.
This module will deal with encrypting and decrypting data and generating secret keys.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""

from django.test import TestCase

from apps.common.utilities.encryption import generate_secret_key


class TestEncryption(TestCase):
    """
        Test Encryption
    """

    def test_generate_secret_key_default(self):
        """
        Test generation of key of size 50.
        :return:
        """

        record = generate_secret_key()
        self.assertIsInstance(record, str)
        self.assertEqual(len(record), 50)

    def test_generate_secret_key_100(self):
        """
        Test generation of key of size 100.
        :return:
        """
        record = generate_secret_key(length=100)
        self.assertIsInstance(record, str)
        self.assertEqual(len(record), 100)

    def test_generate_secret_key_200(self):
        """
        Test generation of key of size 200.
        :return:
        """
        record = generate_secret_key(length=200)
        self.assertIsInstance(record, str)
        self.assertEqual(len(record), 200)

    def test_generate_secret_key_value_error(self):
        """
        Test generation of key too small and expect a value error.
        :return:
        """
        with self.assertRaises(ValueError) as context:
            record = generate_secret_key(length=25)
