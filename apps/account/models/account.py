"""
Account database Model.
This module will contain functions and fields for Account Model.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""
import uuid

from django.db.models import UUIDField, CharField, URLField, DateTimeField, EmailField

from apps.common.globals.database import DEFAULT_CHAR_LEN, MAX_CHAR_LEN
from apps.common.models.base_model import BaseTable


# TODO - Encrypting and Decrypting database fields
# TODO - Hwo to work caching look ups with redis


class Account(BaseTable):
    """
    Account Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = DateTimeField(auto_now=True, help_text="Date account was created.")
    account_name = CharField(max_length=DEFAULT_CHAR_LEN, help_text="Account Name.")
    bio = CharField(
        max_length=MAX_CHAR_LEN, help_text="Short description of the account."
    )
    contact_email = EmailField(
        max_length=DEFAULT_CHAR_LEN, help_text="Account Contact Email."
    )

    website_link = URLField(
        max_length=DEFAULT_CHAR_LEN, blank=True, null=True, help_text="Website Link."
    )
    facebook_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Facebook Social Link.",
    )
    instagram_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Instagram Social Link.",
    )
    twitter_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Twitter Social Link.",
    )
    tiktok_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Tiktok Social Link.",
    )
    linkedin_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="LinkedIn Social Link.",
    )
    snapchat_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Snapchat Social Link.",
    )
    youtube_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Youtube Social Link.",
    )
    twitch_link = URLField(
        max_length=DEFAULT_CHAR_LEN,
        blank=True,
        null=True,
        help_text="Twitch Social Link.",
    )

    def __str__(self):
        return f"{self.account_name}"
