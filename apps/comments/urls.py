"""
Blog URL Model.
This module will contain references for blog urls.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.urls import path

from apps.comments.views import comment_api

urlpatterns = [
    # Blog Post Endpoints
    path("comments", comment_api.CommentListLApi.as_view(), name="CommentListLApiV1"),
    path(
        "comments/user",
        comment_api.CommentUserListLApi.as_view(),
        name="CommentUserListLApiV1",
    ),
    path(
        "comments/view/<uuid:pk>",
        comment_api.CommentDetailApi.as_view(),
        name="CommentDetailApiV1",
    ),
]
