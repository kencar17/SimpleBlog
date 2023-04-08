"""
Category Serializers.
This module will contain user serializers to get, create, update account information.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""
from rest_framework import serializers

from apps.blog.models import Category


class CategoryParentSerializer(serializers.ModelSerializer):
    """
    Category Parent Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Category
        fields = [
            "id",
            "name",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Serializer
    """

    parent = CategoryParentSerializer(
        many=False, help_text="A dictionary containing information about the origin."
    )

    class Meta:
        """
        Meta for Serializer
        """

        model = Category
        fields = [
            "id",
            "created_date",
            "updated_date",
            "name",
            "description",
            "slug",
            "parent",
        ]


class CreateCategorySerializer(serializers.ModelSerializer):
    """
    Create Category Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Category
        fields = ["name", "description", "parent"]
