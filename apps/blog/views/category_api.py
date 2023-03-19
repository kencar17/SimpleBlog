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
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import Category
from apps.blog.serializers.category_serializer import (
    CategorySerializer,
    CreateCategorySerializer,
)
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)

# TODO: How to do delete childs of parents


class CategoryListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]
    serializer_class = CategorySerializer
    create_serializer_class = CreateCategorySerializer

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        categories = Category.objects.all().order_by("-created_date", "name")

        if "category" in self.request.query_params:
            categories = categories.filter(parent=self.request.query_params["category"])

        return categories


class CategoryDetailApi(BlogRetrieveUpdateDestroyMixin):
    """
    Get, update, or delete individual category information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

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
