"""
User Serializers.
This module will contain user serializers to get, create, update user information.
Authors: Kenneth Carmichael (kencar17)
Date: February 10th 2023
Version: 1.0
"""
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import CharField

from apps.account.models import User
from apps.common.globals.database import MIN_PASSWORD_LENGTH


# TODO - Send invite link to user via email to setup password and MFA?


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = [
            "id",
            "account",
            "username",
            "display_name",
            "first_name",
            "last_name",
            "bio",
            "is_contributor",
            "is_editor",
            "is_blog_owner",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def update(self, instance, validated_data) -> User:
        """
        Update user information.
        :param instance: user instance
        :param validated_data: update information
        :return: user instance.
        """

        instance.set_values(pairs=validated_data)
        instance.save()

        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Create User Serializer
    """

    class Meta:
        model = User
        fields = [
            "account",
            "username",
            "display_name",
            "first_name",
            "last_name",
            "bio",
            "is_contributor",
            "is_editor",
        ]

    def create(self, validated_data) -> User:
        """
        Create new user
        :param validated_data: user information
        :return: user instance
        """
        allowed_chars = (
            "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789!@#$%^&*;:"
        )

        validated_data["password"] = User.objects.make_random_password(
            length=MIN_PASSWORD_LENGTH, allowed_chars=allowed_chars
        )
        validated_data["email"] = validated_data["username"]
        user = User.objects.create(**validated_data)
        user.save()

        return user


class UserChangePasswordSerializer(serializers.Serializer):
    """
    Create User Serializer
    """

    password_one = CharField(help_text="Password to change to.")
    password_two = CharField(help_text="Confirm Password.")

    def update(self, instance: User, validated_data):
        """

        :param instance:
        :param validated_data:
        :return:
        """
        errors = dict()
        password_errors = []

        try:
            # validate the password and catch the exception
            validate_password(password=validated_data["password_one"], user=instance)
        except ValidationError as e:
            password_errors.extend(list(e.messages))

        if validated_data["password_one"] != validated_data["password_two"]:
            password_errors.append("Passwords do not match")

        if errors or password_errors:
            errors["password"] = password_errors
            raise serializers.ValidationError(errors)

        instance.set_password(raw_password=validated_data["password_one"])
        instance.save()

        return instance
