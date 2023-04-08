"""
Module for Blog App Admin Config.
This module django Blog App Admin File.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.contrib.admin import register, ModelAdmin

from apps.blog.models import Category, Tag, BlogPost


@register(Category)
class MainCategoryAdmin(ModelAdmin):
    """
    Category Admin Config
    """

    model = Category

    list_display = ("created_date", "name", "description", "slug")
    list_filter = ("name",)
    search_fields = ("name", "description")
    autocomplete_fields = ("parent",)
    ordering = ("-created_date", "name")

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.select_related("parent")


@register(Tag)
class MainTagAdmin(ModelAdmin):
    """
    Tag Admin Config
    """

    model = Tag

    list_display = ("created_date", "name", "description", "slug")
    list_filter = ("name",)
    search_fields = ("name", "description")
    ordering = ("-created_date", "name")


@register(BlogPost)
class MainBlogPostAdmin(ModelAdmin):
    """
    BlogPost Admin Config
    """

    model = BlogPost

    list_display = (
        "account",
        "author",
        "created_date",
        "published_date",
        "status",
        "title",
    )
    list_filter = ("account", "status", "categories", "tags")
    search_fields = ("status", "title", "slug", "excerpt", "content")
    ordering = ("-created_date", "title")
    autocomplete_fields = ("account", "author")
