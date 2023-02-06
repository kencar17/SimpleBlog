"""
User database Model.
This module will contain functions and fields for User Model.
Authors: Kenneth Carmichael (kencar17)
Date: January 16th 2023
Version: 1.0
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import TextField, EmailField, UUIDField, BooleanField, ForeignKey, PROTECT, CharField

from apps.account.managers.user import UserManager
from apps.account.models import Account
from apps.common.globals.database import MAX_CHAR_LEN, DEFAULT_CHAR_LEN
from apps.common.models.base_model import BaseTable


class User(AbstractUser, BaseTable):
    """
    User Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = ForeignKey(Account, on_delete=PROTECT, help_text="Account user belongs too.")
    username = EmailField(
        unique=True,
        help_text="Email field is now username",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    display_name = CharField(default="", max_length=DEFAULT_CHAR_LEN, help_text="Account Display Name", blank=True)
    bio = TextField(default="", max_length=MAX_CHAR_LEN, blank=True)

    is_contributor = BooleanField(
        default=False,
        help_text="Designates whether the user is a contributor to a blog account.",
    )
    is_editor = BooleanField(
        default=False,
        help_text="Designates whether the user is a editor of a blog account.",
    )
    is_blog_owner = BooleanField(
        default=False,
        help_text="Designates whether the user is the blog owner.",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
