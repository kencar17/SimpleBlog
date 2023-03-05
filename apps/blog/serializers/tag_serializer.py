"""
Tag Serializers.
This module will contain tag serializers to get, create, update account information.
Authors: Kenneth Carmichael (kencar17)
Date: March 4th 2023
Version: 1.0
"""
from rest_framework import serializers

from apps.blog.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Tag Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Tag
        fields = [
            "id",
            "created_date",
            "updated_date",
            "name",
            "description",
            "slug",
        ]


class CreateTagSerializer(serializers.ModelSerializer):
    """
    Create Tag Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Tag
        fields = ["name", "description"]
