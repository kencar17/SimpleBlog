"""
User Manager.
This module will contain custom functionality related to user manager. IE Creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 8th 2023
Version: 1.0
"""

from django.contrib.auth.base_user import BaseUserManager

from apps.account.models.queryset.user_queryset import UserQuerySet


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a superuser with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def get_queryset(self):
        """
        Get Queryset and set a default select related for user and account
        :return:
        """
        return UserQuerySet(self.model, using=self._db).select_related("account")

    def contributors(self):
        """
        Get all contributors for a account
        :return: Queryset
        """
        return self.get_queryset().contributors()

    def editors(self):
        """
        Get all editors for a account
        :return: Queryset
        """
        return self.get_queryset().editors()

    def blog_owners(self):
        """
        Get all owners for a account
        :return: Queryset
        """
        return self.get_queryset().blog_owners()
