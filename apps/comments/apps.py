"""
Module for Comments App Config File.
This module django Comments App Config File.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """
    Comments App Config File
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comments"
