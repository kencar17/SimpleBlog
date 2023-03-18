"""
Module for Category Api Endpoints.
This module determines all api endpoints for category model. Supported methods are Get,
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import Category
from apps.blog.serializers.category_serializer import (
    CategorySerializer,
    CreateCategorySerializer,
)
from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class CategoryListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        categories = Category.objects.all().order_by("-created_date", "name")

        if "category" in self.request.query_params:
            categories = categories.filter(parent=self.request.query_params["category"])

        return categories

    def get(self, request, *args, **kwargs):
        """
        Get Categories for the system
        :param request: request
        :return: Json list of categories.
        """

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)

        if not page:
            serializer = CategorySerializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = CategorySerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new category.
        :param request: request
        :return: Json of category.
        """

        json_data = request.data
        serializer = CreateCategorySerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            user = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=CategorySerializer(user, many=False).data)


class CategoryDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual category information.
    """

    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            category = Category.objects.select_related("parent").get(
                pk=self.kwargs["pk"]
            )
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, category)

        return category

    def get(self, request, *args, **kwargs):
        """
        Get category information.
        :param request: request
        :return: category Json.
        """

        serializer = CategorySerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update Category Information.
        :param request: request
        :return: Category json.
        """

        json_data = request.data
        serializer = CategorySerializer(data=json_data, many=False, partial=True)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            serializer.instance = serializer.update(
                instance=self.get_object(), validated_data=serializer.validated_data
            )
        except ValidationError as exc:
            message = {"message": "Update failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Delete Category
        :param request: request
        :return: Message indicating Success
        """
        # TODO: How to do delete childs of parents
        category = self.get_object()
        category.delete()

        return json_response(data={"message": "category has been deleted."})
