"""
Module for Blog App Config File.
This module django Blog App Config File.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Blog App Config File
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog"
