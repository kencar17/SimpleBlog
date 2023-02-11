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
    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            type=str,
            help="Must be email. Password will be auto gen.",
        )

    def handle(self, *args, **options) -> None:
        """
        Generate secret keys for project.
        :param args:
        :param options:
        :return:
        """

        initial_account = {
            "account_name": "My Account",
            "bio": "Am a bio",
            "contact_email": "email@email.com",
        }

        initial_user = {
            "username": options["email"],
            "first_name": "First",
            "last_name": "Last",
            "is_staff": True,
            "is_superuser": True,
        }

        account = Account.create(param_dict=initial_account)
        account.save()

        initial_user["account"] = account

        user = User.create(param_dict=initial_user)
        password = User.objects.make_random_password()
        user.account = account
        user.set_password(raw_password=password)
        user.save()

        print(f"Initial Account Created with id: {account.id}")
        print(f"User password: {password}")
        print("Please ensure you update superuser and default account.")
