"""
Module for User Api Endpoints.
This module determines all api endpoints for user model. Supported methods are Get, Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: February 8th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.account.models import User
from apps.account.serializers.user_serializer import (
    UserSerializer,
    CreateUserSerializer,
)
from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import default_pagination, json_response


# TODO - Account Filtering of users
# TODO - Password reset Endpoint


class UserListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new user with auto gen password.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "display_name", "fist_name", "last_name", "bio"]

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

    def get(self, request, *args, **kwargs):
        """
        Get users for the system or an account.
        :param request: request
        :return: Json list of Users.
        """

        users = self.get_queryset()

        users = self.filter_queryset(queryset=users)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=users, request=request)

        if not page:
            serializer = UserSerializer(users, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = UserSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new user.
        :param request: request
        :return: Json of user.
        """

        json_data = request.data
        serializer = CreateUserSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            user = serializer.create(validated_data=serializer.validated_data)
        except (ValidationError, IntegrityError) as e:
            message = {"user": f"User creation failed: {str(e)}"}
            return json_response(message=message, error=True)

        return json_response(data=UserSerializer(user, many=False).data)


class UserDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual user information.
    """

    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            user = User.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            raise Http404

        return user

    def get(self, request, *args, **kwargs):
        """
        Get user information.
        :param request: request
        :return: User Json.
        """

        serializer = UserSerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update User Information.
        :param request: request
        :return: User json.
        """

        json_data = request.data
        serializer = UserSerializer(data=json_data, many=False, partial=True)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            serializer.instance = serializer.update(
                instance=self.get_object(), validated_data=serializer.validated_data
            )
        except ValidationError as e:
            message = {"user": f"User update failed: {str(e)}"}
            return json_response(message=message, error=True)

        return json_response(data=serializer.data)

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
