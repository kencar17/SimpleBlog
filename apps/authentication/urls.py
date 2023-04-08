"""
Authentication URLs.
This module will contain authentication endpoints and anything relate to user management.
Authors: Kenneth Carmichael (kencar17)
Date: January 26th 2023
Version: 1.0
"""
from django.urls import path


from apps.authentication.views.token_view import (
    BlogTokenObtainPairView,
    BlogTokenRefreshView,
)

urlpatterns = [
    path("token", BlogTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", BlogTokenRefreshView.as_view(), name="token_refresh"),
]
