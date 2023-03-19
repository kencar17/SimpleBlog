"""
Module for Blog Post Api Endpoints.
This module determines all api endpoints for blog post model. Supported methods are Get,
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import BlogPost
from apps.blog.serializers.blog_serializers import (
    BlogPostSerializer,
    BlogPostExcerptSerializer,
    CreateBlogPostSerializer,
)
from apps.common.mixins.list_create_mixin import BlogListCreateMixin
from apps.common.mixins.retrieve_update_destroy_mixin import (
    BlogRetrieveUpdateDestroyMixin,
)


class BlogListLApi(BlogListCreateMixin):
    """
    Get a List of users bases on query params, or create a new blog post.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "excerpt"]
    ordering_fields = [
        "created_date",
        "updated_date",
        "published_date",
        "status",
        "title",
    ]
    serializer_class = BlogPostExcerptSerializer
    create_serializer_class = CreateBlogPostSerializer

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        ordering = self.request.query_params.get("ordering", "-created_date")
        blogs = (
            BlogPost.objects.select_related("account", "author")
            .all()
            .order_by(ordering)
        )

        if "status" in self.request.query_params:
            blogs = blogs.filter(status=self.request.query_params["status"])

        if "is_featured" in self.request.query_params:
            blogs = blogs.filter(is_featured=self.request.query_params["is_featured"])

        if "account" in self.request.query_params:
            blogs = blogs.filter(account=self.request.query_params["account"])

        if "author" in self.request.query_params:
            blogs = blogs.filter(author=self.request.query_params["author"])

        return blogs


class BlogDetailApi(BlogRetrieveUpdateDestroyMixin):
    """
    Get, update, or delete individual blog post information.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = BlogPostSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        try:
            blog = BlogPost.objects.select_related("account", "author").get(
                pk=self.kwargs["pk"]
            )
        except ObjectDoesNotExist as exc:
            raise Http404 from exc

        # May raise a permission denied
        self.check_object_permissions(self.request, blog)

        return blog
