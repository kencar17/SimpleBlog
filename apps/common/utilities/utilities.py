"""
Module for Utility functions.
This module will contain Utility functions that are used throughout the project.
Authors: Kenneth Carmichael (kencar17)
Date: January 16th 2023
Version: 1.0
"""
from typing import Union

from django.http import JsonResponse
from rest_framework import status


def json_response(
    data: Union[list, dict] = None,
    error: bool = False,
    message: dict = None,
    http_status=status.HTTP_200_OK,
) -> JsonResponse:
    """
    Format Api response for all api endpoints.
    :param data: Response Data
    :param error: is error boolean
    :param message: Error messages
    :param http_status: status code, default to 200
    :return: Json Response of results
    """
    if data is None:
        data = {}
    if message is None:
        message = {}

    return JsonResponse(
        {"is_error": error, "message": message, "content": data},
        status=http_status,
        safe=False,
    )
