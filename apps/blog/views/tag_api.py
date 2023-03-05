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
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.models import Tag
from apps.blog.serializers.tag_serializer import TagSerializer, CreateTagSerializer

from apps.common.pagination.paginations import ApiPagination
from apps.common.utilities.utilities import json_response, default_pagination


class TagListLApi(ListCreateAPIView):
    """
    Get a List of users bases on query params, or create a new account.
    """

    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]
    queryset = Tag.objects.all().order_by("-created_date", "name")

    def get(self, request, *args, **kwargs):
        """
        Get Tags for the system
        :param request: request
        :return: Json list of tags.
        """

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset=queryset)
        pagination = ApiPagination()
        page = pagination.paginate_queryset(queryset=queryset, request=request)

        if not page:
            serializer = TagSerializer(queryset, many=True)
            return json_response(data=default_pagination(data=serializer.data))

        serializer = TagSerializer(page, many=True)

        return json_response(data=pagination.get_paginated_response(serializer.data))

    def post(self, request, *args, **kwargs):
        """
        Create a new tag.
        :param request: request
        :return: Json of tag.
        """

        json_data = request.data
        serializer = CreateTagSerializer(data=json_data, many=False)

        if not serializer.is_valid():
            return json_response(message=serializer.errors, error=True)

        try:
            user = serializer.create(validated_data=serializer.validated_data)
        except ValidationError as exc:
            message = {"message": "Creation Failed", "errors": exc.detail}
            return json_response(message=message, error=True)

        return json_response(data=TagSerializer(user, many=False).data)


class TagDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete individual category information.
    """

    authentication_classes = [JWTAuthentication]

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

    def get(self, request, *args, **kwargs):
        """
        Get tag information.
        :param request: request
        :return: tag Json.
        """

        serializer = TagSerializer(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update tag Information.
        :param request: request
        :return: tag json.
        """

        json_data = request.data
        serializer = TagSerializer(data=json_data, many=False, partial=True)

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
        Delete tag
        :param request: request
        :return: Message indicating Success
        """
        tag = self.get_object()
        tag.delete()

        return json_response(data={"message": "tag has been deleted."})
