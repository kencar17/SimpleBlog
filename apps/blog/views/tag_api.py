"""
Module for Tag Api Endpoints.
This module determines all api endpoints for tag model. Supported methods are Get,
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 4th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import Tag
from apps.blog.serializers.tag_serializer import TagSerializer, CreateTagSerializer
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)


class TagListLApi(BlogListCreateMixin, ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    serializer_class = TagSerializer
    create_serializer_class = CreateTagSerializer
    queryset = Tag.objects.all().order_by("-created_date", "name")


class TagDetailApi(BlogRetrieveUpdateDestroyMixin, RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual category information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            tag = Tag.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, tag)

        return tag
