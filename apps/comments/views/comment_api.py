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
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.comments.models import Comment
from apps.comments.serializers.comment_serializers import (
    CreateCommentSerializer,
    CommentSerializer,
)

from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class CommentListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        blog_id = self.request.query_params.get("blog")

        if blog_id is None:
            raise ValidationError('"blog" id is required param.')

        comments = Comment.objects.filter(blog__pk=blog_id).order_by("-created_date")

        return comments

    def get(self, request, *args, **kwargs):
        """
        Get comments for the system
        :param request: request
        :return: Json list of comments.
        """

        try:
            queryset = self.get_queryset()
        except ValidationError as exc:
            message = {"message": "Get Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)

        if not page:
            serializer = CommentSerializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = CommentSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new comment.
        :param request: request
        :return: Json of comment.
        """

        json_data = request.data
        serializer = CreateCommentSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            user = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=CommentSerializer(user, many=False).data)


class CommentUserListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def get_queryset(self):
        """
        This view should return a list of all users and perform any additional filtering.
        """
        user_id = self.request.query_params.get("user")

        if user_id is None:
            raise ValidationError('"user" id is required param.')

        comments = Comment.objects.filter(author__pk=user_id).order_by("-created_date")

        return comments

    def get(self, request, *args, **kwargs):
        """
        Get comments for the system
        :param request: request
        :return: Json list of comments.
        """

        try:
            queryset = self.get_queryset()
        except ValidationError as exc:
            message = {"message": "Get Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)

        if not page:
            serializer = CommentSerializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = CommentSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))


class CommentDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual comment information.
    """

    authentication_classes = [JWTAuthentication]

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

    def get(self, request, *args, **kwargs):
        """
        Get comment information.
        :param request: request
        :return: comment Json.
        """

        serializer = CommentSerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update comments Information.
        :param request: request
        :return: Comment json.
        """

        json_data = request.data
        serializer = CommentSerializer(data=json_data, many=False, partial=True)

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
        Delete comment
        :param request: request
        :return: Message indicating Success
        """

        self.get_object().delete()

        return json_response(data={"message": "Comment has been deleted."})
