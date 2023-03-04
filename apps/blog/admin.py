"""
Module for Blog App Admin Config.
This module django Blog App Admin File.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""

from django.contrib.admin import register, ModelAdmin

from apps.blog.models import Category


# Register your models here.


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
