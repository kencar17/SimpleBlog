"""
Category database Model.
This module will contain functions and fields for Category Model.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""
import uuid

from django.db.models import (
    UUIDField,
    CharField,
    DateTimeField,
    SlugField,
    ForeignKey,
    PROTECT,
)
from django.template.defaultfilters import slugify
from django.utils import timezone

from apps.common.globals.database import DEFAULT_CHAR_LEN, MIN_CHAR_LEN
from apps.common.models.base_model import BaseTable


class Category(BaseTable):
    """
    Category Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = DateTimeField(auto_now=True, help_text="Date category was created.")
    updated_date = DateTimeField(
        help_text="Date category was updated.", null=True, blank=True
    )
    name = CharField(
        unique=True,
        default="",
        max_length=MIN_CHAR_LEN,
        help_text="Category Name.",
    )
    description = CharField(
        max_length=DEFAULT_CHAR_LEN, help_text="Description or summary of the category."
    )
    slug = SlugField(
        unique=True,
        max_length=MIN_CHAR_LEN,
        help_text="Description or summary of the category.",
        blank=True,
    )

    parent = ForeignKey(
        "Category",
        on_delete=PROTECT,
        help_text="A reference to another category model that represents the "
        "parent category, if the category is a subcategory of another category.",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs) -> None:
        self.clean_fields()
        self.updated_date = timezone.now()
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
