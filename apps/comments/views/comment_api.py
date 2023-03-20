"""
Module for Comment Api Endpoints.
This module determines all api endpoints for comment model. Supported methods are Get,
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.comments.models import Comment
from apps.comments.serializers.comment_serializers import (
    CreateCommentSerializer,
    CommentSerializer,
)
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)


class CommentListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    serializer_class = CommentSerializer
    create_serializer_class = CreateCommentSerializer

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        blog_id = self.request.query_params.get("blog")

        if blog_id is None:
            raise ValidationError('"blog" id is required param.')

        comments = Comment.objects.filter(blog__pk=blog_id).order_by("-created_date")

        return comments


class CommentUserListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new account.
    """

    http_method_names = ["get"]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        user_id = self.request.query_params.get("user")

        if user_id is None:
            raise ValidationError('"user" id is required param.')

        comments = Comment.objects.filter(author__pk=user_id).order_by("-created_date")

        return comments


class CommentDetailApi(BlogRetrieveUpdateDestroyMixin):
    """
    Get, update, or delete individual comment information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            category = Comment.objects.select_related("parent").get(
                pk=self.kwargs["pk"]
            )
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, category)

        return category
