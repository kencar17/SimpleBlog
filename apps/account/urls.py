"""
User database Model.
This module will contain functions and fields for User Model.
Authors: Kenneth Carmichael (kencar17)
Date: January 16th 2023
Version: 1.0
"""

from django.urls import path

from apps.account.views import user_api

urlpatterns = [
    # User Endpoints
    path("users", user_api.UserListLApi.as_view(), name="UserListLApiV1"),
    path("users/<uuid:pk>", user_api.UserDetailApi.as_view(), name="UserDetailApiV1"),
    path(
        "users/<uuid:pk>/change_password",
        user_api.UserPasswordChangeApi.as_view(),
        name="UserDetailApiV1",
    ),
]
