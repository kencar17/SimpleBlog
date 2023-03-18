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
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import BlogPost
from apps.blog.serializers.blog_serializers import (
    BlogPostSerializer,
    BlogPostExcerptSerializer,
    CreateBlogPostSerializer,
)

from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class BlogListLApi(ListCreateAPIView):
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

    def get(self, request, *args, **kwargs):
        """
        Get blog posts for the system
        :param request: request
        :return: Json list of blog posts.
        """

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)

        if not page:
            serializer = BlogPostExcerptSerializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = BlogPostExcerptSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new blog post.
        :param request: request
        :return: Json of blog post.
        """

        json_data = request.data
        serializer = CreateBlogPostSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            blog = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=BlogPostSerializer(blog, many=False).data)


class BlogDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual blog post information.
    """

    authentication_classes = [JWTAuthentication]

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

    def get(self, request, *args, **kwargs):
        """
        Get blog post information.
        :param request: request
        :return: blog post Json.
        """

        serializer = BlogPostSerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update blog post Information.
        :param request: request
        :return: blog post json.
        """

        json_data = request.data
        serializer = BlogPostSerializer(data=json_data, many=False, partial=True)

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
        Delete blog post
        :param request: request
        :return: Message indicating Success
        """
        self.get_object().delete()

        return json_response(data={"message": "Blog post has been deleted."})
