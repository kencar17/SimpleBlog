"""
Module for Comment App Admin Config.
This module django comment App Admin File.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""

from django.contrib.admin import register, ModelAdmin

from apps.comments.models import Comment


@register(Comment)
class MainCommentAdmin(ModelAdmin):
    """
    Comment Admin Config
    """

    model = Comment

    list_display = ("created_date", "blog", "author", "parent", "content")
    list_filter = ("blog", "author")
    search_fields = ("name", "description")
    autocomplete_fields = ("blog", "author", "parent")
    ordering = ("-created_date", "blog")

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.select_related("parent")
