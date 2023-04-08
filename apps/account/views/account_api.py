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
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.account.models import Account
from apps.account.serializers.account_serializer import (
    AccountSerializer,
    CreateAccountSerializer,
)
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)
from apps.common.utilities.utilities import json_response


class AccountListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["account_name", "bio", "contact_email"]
    queryset = Account.objects.all().order_by("-created_date", "account_name")

    serializer_class = AccountSerializer
    create_serializer_class = CreateAccountSerializer


class AccountDetailApi(BlogRetrieveUpdateDestroyMixin):
    """
    Get, update, or delete individual account information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = AccountSerializer

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
