"""
Module for Comments App Admin Config.
This module django comments App Admin File.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""
import uuid

from django.db.models import ForeignKey, TextField, DateTimeField, CASCADE, UUIDField

from apps.account.models import User
from apps.blog.models import BlogPost
from apps.common.globals.database import DEFAULT_CHAR_LEN
from apps.common.models.base_model import BaseTable


class Comment(BaseTable):
    """
    Comment Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = DateTimeField(auto_now=True, help_text="Date blog post was created.")
    blog = ForeignKey(
        BlogPost, on_delete=CASCADE, help_text="Blog Post comment is for."
    )
    author = ForeignKey(User, on_delete=CASCADE, help_text="Author of the comment")
    parent = ForeignKey(
        "Comment",
        null=True,
        blank=True,
        related_name="children",
        on_delete=CASCADE,
        help_text="Parent Comment for comment, otherwise none is no parent.",
    )
    content = TextField(
        default="", max_length=DEFAULT_CHAR_LEN, help_text="Comment Content."
    )

    def __str__(self):
        return f"{self.blog} - {self.author}: {self.content}"
