"""
Module for JWT Token Views.
This module determines all api endpoints for JWT Tokens getting and refreshing.
Authors: Kenneth Carmichael (kencar17)
Date: January 26th 2023
Version: 1.0
"""
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.serializers.token_serializers import (
    BlogTokenObtainPairSerializer,
    BlogTokenRefreshSerializer,
)
from apps.common.utilities.utilities import json_response


class BlogTokenObtainPairView(TokenObtainPairView):
    """
    Get Blog Token Obtain Pair View
    """

    serializer_class = BlogTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and get access token and refresh token
        :param request: Request
        :param args:
        :param kwargs:
        :return: Json Response of Token info
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exe:
            raise InvalidToken(exe.args[0]) from exe

        return json_response(data=serializer.validated_data)


class BlogTokenRefreshView(TokenRefreshView):
    """
    Blog Token Refresh View
    """

    serializer_class = BlogTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        Refresh access token and get new refresh token
        :param request: Request
        :param args:
        :param kwargs:
        :return: Json Response of Token info
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exe:
            raise InvalidToken(exe.args[0]) from exe

        return json_response(data=serializer.validated_data)
