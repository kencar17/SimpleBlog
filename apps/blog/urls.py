"""
Blog URL Model.
This module will contain references for blog urls.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.urls import path

from apps.blog.views import category_api, tag_api

urlpatterns = [
    # Category Endpoints
    path(
        "categories", category_api.CategoryListLApi.as_view(), name="CategoryListLApiV1"
    ),
    path(
        "categories/<uuid:pk>",
        category_api.CategoryDetailApi.as_view(),
        name="CategoryDetailApiV1",
    ),
    # Tag Endpoints
    path("tags", tag_api.TagListLApi.as_view(), name="TagListLApiV1"),
    path(
        "tags/<uuid:pk>",
        tag_api.TagDetailApi.as_view(),
        name="TagDetailApiV1",
    ),
]
