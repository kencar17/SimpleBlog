"""
Module for User Api Endpoints.
This module determines all api endpoints for user model. Supported methods are
Get, Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: February 8th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.account.models import User
from apps.account.serializers.user_serializer import (
    UserSerializer,
    CreateUserSerializer,
    UserChangePasswordSerializer,
)
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)
from apps.common.utilities.utilities import json_response


# TODO: Account Filtering of users


class UserListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new user with auto gen password.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "display_name", "fist_name", "last_name", "bio"]

    serializer_class = UserSerializer
    create_serializer_class = CreateUserSerializer

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        users = User.objects.all().order_by("-last_login", "first_name", "last_name")

        if "is_contributor" in self.request.query_params:
            users = users.filter(
                is_contributor=self.request.query_params["is_contributor"]
            )

        if "is_editor" in self.request.query_params:
            users = users.filter(is_editor=self.request.query_params["is_editor"])

        if "is_blog_owner" in self.request.query_params:
            users = users.filter(
                is_contributor=self.request.query_params["is_blog_owner"]
            )

        if "is_staff" in self.request.query_params:
            users = users.filter(is_staff=self.request.query_params["is_staff"])

        if "is_superuser" in self.request.query_params:
            users = users.filter(is_superuser=self.request.query_params["is_superuser"])

        if "is_active" in self.request.query_params:
            users = users.filter(is_active=self.request.query_params["is_active"])

        return users


class UserDetailApi(BlogRetrieveUpdateDestroyMixin):
    """
    Get, update, or delete individual user information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            user = User.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, user)

        return user

    def delete(self, request, *args, **kwargs):
        """
        Deactivated User
        :param request: request
        :return: Message indicating Success
        """

        user = self.get_object()
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()

        return json_response(data={"message": "User has been deactivated."})


class UserPasswordChangeApi(UpdateAPIView):
    """
    Update user password.
    """

    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            user = User.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, user)

        return user

    def put(self, request, *args, **kwargs):
        """
        Update user password.
        :param request: request
        :return: Success Message.
        """

        json_data = request.data
        serializer = UserChangePasswordSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            _ = serializer.update(
                instance=self.get_object(), validated_data=serializer.validated_data
            )
        except ValidationError as exc:
            message = {"message": "Password Change Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data={"message": "User password has been changed."})
