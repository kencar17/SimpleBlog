"""
User database Model.
This module will contain functions and fields for User Model.
Authors: Kenneth Carmichael (kencar17)
Date: January 16th 2023
Version: 1.0
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import TextField, EmailField, UUIDField

from apps.authentication.managers.user import UserManager


class User(AbstractUser):
    """
    User Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = EmailField(
        unique=True,
        help_text="Email field is now username",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    bio = TextField(default="", max_length=200, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    # Override
    def __repr__(self) -> str:
        return f"< User ( {self.first_name} {self.last_name} ) >"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
