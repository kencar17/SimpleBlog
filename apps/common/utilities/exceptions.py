"""
Module for custom exception handler.
This module determines all api endpoints for contact model. Supported methods are Get, Post, Put, and Delete.
Authors: Kenneth Carmichael (kencar17)
Date: January 16th 2023
Version: 1.0
"""
from rest_framework.views import exception_handler

from apps.common.utilities.utilities import json_response


def blog_exception_handler(exc, context):
    """
    Custom Exception Handling, default to internal server error.
    :param exc:
    :param context:
    :return:
    """
    # Call REST framework's default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    if not response:
        return json_response(
            data={},
            message={"message": "Internal Server Error", "errors": []},
            error=True,
        )

    response.data = {
        "is_error": True,
        "error": {"message": response.data.get("detail", ""), "errors": [exc]},
        "content": {},
    }

    return response
