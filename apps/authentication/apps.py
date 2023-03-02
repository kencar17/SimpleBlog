"""
Module for authentication App Config File.
This module django authentication App Config File.
Authors: Kenneth Carmichael (kencar17)
Date: February 26th 2023
Version: 1.0
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    authentication App Config File
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"
