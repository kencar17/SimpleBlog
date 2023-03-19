"""
Module for Blog Retrieve Update Destroy Mixin.
This module contains commons get, put, and delete views for api endpoints.
Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th, 2023
Version: 1.0
"""
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.common.utilities.utilities import json_response


class BlogRetrieveUpdateDestroyMixin(RetrieveUpdateDestroyAPIView):
    """
    Blog Retrieve Update Destroy Mixin
    """

    def get(self, request, *args, **kwargs):
        """
        Get instance information.
        :param request: request
        :return: Instance Json.
        """

        serializer = self.serializer_class(self.get_object(), many=False)

        return json_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update instance Information.
        :param request: request
        :return: Instance json.
        """

        json_data = request.data
        serializer = self.serializer_class(data=json_data, many=False, partial=True)

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
        Delete Instance
        :param request: request
        :return: Message indicating Success
        """
        self.get_object().delete()

        return json_response(data={"message": "Instance has been deleted."})
