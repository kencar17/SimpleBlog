"""
Module for Account Api Endpoints.
This module determines all api endpoints for account model. Supported methods are Get,
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: February 26th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.account.models import Account
from apps.account.serializers.account_serializer import (
    AccountSerializer,
    CreateAccountSerializer,
)
from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class AccountListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["account_name", "bio", "contact_email"]
    queryset = Account.objects.all().order_by("-created_date", "account_name")

    def get(self, request, *args, **kwargs):
        """
        Get accounts for the system
        :param request: request
        :return: Json list of Accounts.
        """

        accounts = self.get_queryset()
        accounts = self.filter_queryset(queryset=accounts)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=accounts, request=request)

        if not page:
            serializer = AccountSerializer(accounts, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = AccountSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new account.
        :param request: request
        :return: Json of account.
        """

        json_data = request.data
        serializer = CreateAccountSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            user = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Account Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=AccountSerializer(user, many=False).data)


class AccountDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual account information.
    """

    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            account = Account.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, account)

        return account

    def get(self, request, *args, **kwargs):
        """
        Get account information.
        :param request: request
        :return: account Json.
        """

        serializer = AccountSerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update account Information.
        :param request: request
        :return: account json.
        """

        json_data = request.data
        serializer = AccountSerializer(data=json_data, many=False, partial=True)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            serializer.instance = serializer.update(
                instance=self.get_object(), validated_data=serializer.validated_data
            )
        except ValidationError as exc:
            message = {"message": "Account update failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Deactivated account
        :param request: request
        :return: Message indicating Success
        """

        account = self.get_object()
        account.is_active = False
        account.save()

        return json_response(data={"message": "Account has been deactivated."})
