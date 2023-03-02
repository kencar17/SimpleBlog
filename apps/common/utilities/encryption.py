"""
Module for encryption.
This module will deal with encrypting and decrypting data and generating secret keys.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""
from django.core.management.utils import get_random_string


def generate_secret_key(length: int = 50) -> str:
    """
    Generate Secret Keys for project.
    :return: Random Generate Key
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"

    if length < 50:
        raise ValueError(
            "The 'length' is too small, must be greater then or equal to 50."
        )

    return get_random_string(length=length, allowed_chars=chars)
