"""
Blog Serializers.
This module will contain blog serializers to get, create, update account information.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""
from rest_framework import serializers

from apps.blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    BlogPost Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = BlogPost
        fields = [
            "id",
            "account",
            "author",
            "created_date",
            "updated_date",
            "published_date",
            "status",
            "views",
            "likes",
            "dislikes",
            "title",
            "slug",
            "excerpt",
            "categories",
            "tags",
            "is_featured",
            "content",
        ]


class BlogPostExcerptSerializer(serializers.ModelSerializer):
    """
    BlogPost Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = BlogPost
        fields = [
            "id",
            "account",
            "author",
            "created_date",
            "updated_date",
            "published_date",
            "status",
            "views",
            "likes",
            "dislikes",
            "title",
            "slug",
            "excerpt",
            "categories",
            "tags",
            "is_featured",
        ]


class CreateBlogPostSerializer(serializers.ModelSerializer):
    """
    Create BlogPost Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = BlogPost
        fields = [
            "account",
            "author",
            "status",
            "title",
            "excerpt",
            "categories",
            "tags",
            "is_featured",
            "content",
        ]
