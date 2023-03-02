"""
Account Serializers.
This module will contain user serializers to get, create, update account information.
Authors: Kenneth Carmichael (kencar17)
Date: February 28th 2023
Version: 1.0
"""
from rest_framework import serializers

from apps.account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Account
        fields = [
            "id",
            "created_date",
            "account_name",
            "bio",
            "contact_email",
            "website_link",
            "facebook_link",
            "instagram_link",
            "twitter_link",
            "tiktok_link",
            "linkedin_link",
            "snapchat_link",
            "youtube_link",
            "twitch_link",
            "is_active",
        ]


class CreateAccountSerializer(serializers.ModelSerializer):
    """
    Create Account Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Account
        fields = ["account_name", "contact_email", "bio"]
