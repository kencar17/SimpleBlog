"""
Module for custom pagination for api responses.
This module sets the pagination parameters, limitations, and response structure for the project. Any pagination
should follow this structure.
Authors: Kenneth Carmichael (kencar17)
Date: January 26th 2023
Version: 1.0
"""
import math

from rest_framework import pagination


class ApiPagination(pagination.PageNumberPagination):
    """
    Custom pagination class
    """

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data) -> dict:
        """
        Format pagination response into a standard format with response fields.
        :param data: QuerySet data
        :return: Dictionary of pagination results.
        """

        pages = math.ceil(
            self.page.paginator.count
            / int(self.request.query_params.get("page_size", self.page_size))
        )

        return {
            "count": self.page.paginator.count,
            "pages": pages,
            "current": self.page.number,
            "previous": self.get_previous_link(),
            "next": self.get_next_link(),
            "results": data,
        }
