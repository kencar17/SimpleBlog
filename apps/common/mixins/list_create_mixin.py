"""
Module for Blog List Create Mixin.
This module contains commons get and create views for api endpoints.
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th, 2023
Version: 1.0
"""
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView

from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class BlogListCreateMixin(ListCreateAPIView):
    """
    Mixin
    """

    create_serializer_class = None

    def get_create_serializer(self):
        """
        Get Create serializer
        :return:
        """
        return self.create_serializer_class

    def get(self, request, *args, **kwargs):
        """
        Get instances for the system
        :param request: request
        :return: Json list of instances.
        """

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)
        serializer = self.get_serializer_class()

        if not page:
            serializer = serializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = serializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new instance.
        :param request: request
        :return: Json of instance.
        """

        json_data = request.data
        serializer = self.get_create_serializer()
        serializer = serializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            instance = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        serializer = self.get_serializer_class()

        return json_response(data=serializer(instance, many=False).data)
