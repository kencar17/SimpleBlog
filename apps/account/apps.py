"""
Module for Account App Config File.
This module django Account App Config File.
Authors: Kenneth Carmichael (kencar17)
Date: February 26th 2023
Version: 1.0
"""

from django.apps import AppConfig


class AccountConfig(AppConfig):
    """
    Account App Config File
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
