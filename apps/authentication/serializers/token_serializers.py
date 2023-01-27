"""
Module for JWT Token Serializers.
This module will serialize all token requests.
Authors: Kenneth Carmichael (kencar17)
Date: January 26th 2023
Version: 1.0
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class BlogTokenObtainPairSerializer(TokenObtainSerializer):
    """
    Blog Token Obtain Pair Serializer
    """

    token_class = RefreshToken

    def validate(self, attrs):
        """
        Validate Token Refresh request and refresh the token
        :param attrs:
        :return: Token data
        """
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["iat"] = refresh.payload["iat"]
        data["expiry"] = refresh.payload["exp"]

        return data


class BlogTokenRefreshSerializer(serializers.Serializer):
    """
    Blog Token Refresh Serializer
    """

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs) -> dict:
        """
        Validate Token Refresh request and refresh the token
        :param attrs:
        :return: Token data
        """
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            print(api_settings.ROTATE_REFRESH_TOKENS)
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
            data["iat"] = refresh.payload["iat"]
            data["expiry"] = refresh.payload["exp"]

        return data
