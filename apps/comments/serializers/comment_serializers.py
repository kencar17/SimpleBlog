"""
Comment Serializers.
This module will contain user serializers to get, create, update comment information.
Authors: Kenneth Carmichael (kencar17)
Date: March 18th 2023
Version: 1.0
"""
from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """

    children = serializers.SerializerMethodField(
        "get_children_comments", help_text="A list of child comments.", required=False
    )

    class Meta:
        """
        Meta for Serializer
        """

        model = Comment
        fields = [
            "id",
            "created_date",
            "blog",
            "author",
            "parent",
            "content",
            "children",
        ]

    @staticmethod
    def get_children_comments(instance):
        """
        Get child elements for comment
        :param instance: comment instance
        :return: list of comment childs
        """
        comments = instance.children.all().order_by("created_date")
        return CommentSerializer(comments, many=True).data


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Create Comment Serializer
    """

    class Meta:
        """
        Meta for Serializer
        """

        model = Comment
        fields = ["blog", "author", "content", "parent"]
