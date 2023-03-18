"""
Blog Post database Model.
This module will contain functions and fields for Blog Post Model.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""
import uuid

from django.db.models import (
    UUIDField,
    CharField,
    IntegerField,
    TextField,
    BooleanField,
    DateTimeField,
    SlugField,
    ForeignKey,
    ManyToManyField,
    PROTECT,
)
from django.template.defaultfilters import slugify
from django.utils import timezone

from apps.account.models import Account, User
from apps.blog.models import Tag, Category
from apps.common.globals.database import MIN_CHAR_LEN, MAX_CHAR_LEN, MAX_TEXT_LEN
from apps.common.models.base_model import BaseTable


# TODO: Add Image/Thumbnail


class BlogPost(BaseTable):
    """
    Blog Post Model
    """

    choices = (("DRAFT", "Draft"), ("PUBLISHED", "Published"), ("ARCHIVED", "Archived"))

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    account = ForeignKey(
        Account, on_delete=PROTECT, help_text="Account blog post belongs too."
    )
    author = ForeignKey(User, on_delete=PROTECT, help_text="Author of the blog post.")

    created_date = DateTimeField(auto_now=True, help_text="Date blog post was created.")
    updated_date = DateTimeField(
        help_text="Date blog post was updated.", null=True, blank=True
    )
    published_date = DateTimeField(
        help_text="Date blog post was published.", null=True, blank=True
    )

    status = CharField(
        choices=choices, max_length=MIN_CHAR_LEN, help_text="Status of the blog post."
    )
    views = IntegerField(
        default=0, help_text="Number of times the blog post has been viewed"
    )
    likes = IntegerField(
        default=0, help_text="Number of times the blog post has been liked by users"
    )
    dislikes = IntegerField(
        default=0, help_text="Number of times the blog post has been disliked by users"
    )

    title = CharField(max_length=MIN_CHAR_LEN, help_text="Title of the blog post")
    slug = SlugField(
        max_length=MIN_CHAR_LEN, help_text="URL Safe slug of the title.", blank=True
    )
    excerpt = CharField(
        default="", max_length=MAX_CHAR_LEN, help_text="Excerpt of the blog post."
    )
    content = TextField(
        default="", max_length=MAX_TEXT_LEN, help_text="Content of the blog post."
    )

    categories = ManyToManyField(
        Category, help_text="Categories of the blog post", blank=True
    )
    tags = ManyToManyField(Tag, help_text="tags of the blog post", blank=True)

    is_featured = BooleanField(
        default=False, help_text="Is the blog post a featured post."
    )

    def save(self, *args, **kwargs) -> None:
        self.clean_fields()
        self.updated_date = timezone.now()
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account} - {self.author}: {self.title}"
