"""
Module for initial config of the project.
This module will be a management command that will generate initial account for admin.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""

from django.core.management import BaseCommand

from apps.account.models import Account, User


class Command(BaseCommand):
    """
    Django Management command to initialize the project
    """

    def add_arguments(self, parser):
        """
        Add arguements for the command
        :param parser:
        :return:
        """
        parser.add_argument(
            "email",
            type=str,
            help="Must be email. Password will be auto gen.",
        )

    def handle(self, *args, **options) -> None:
        """
        Generate secret keys for project
        :param args:
        :param options:
        :return:
        """

        initial_account = {
            "account_name": "My Account",
            "bio": "Am a bio",
            "contact_email": "email@email.com",
        }

        account = Account.objects.create(**initial_account)
        account.save()

        password = User.objects.make_random_password(
            length=16,
            allowed_chars="abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789!@#$%^&*;:",
        )

        initial_user = {
            "account": account,
            "username": options["email"],
            "first_name": "First",
            "last_name": "Last",
            "is_staff": True,
            "is_superuser": True,
            "password": password,
        }

        user = User.objects.create(**initial_user)
        user.save()

        print(f"Initial Account Created with id: {account.id}")
        print(f"User password: {password}")
        print("Please ensure you update superuser and default account.")
