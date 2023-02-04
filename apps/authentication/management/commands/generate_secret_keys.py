"""
Module for Generate Keys Command.
This module will be a management command that will generate the necessary secret keys for the project.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""

from cryptography.fernet import Fernet
from django.core.management import BaseCommand

from apps.common.utilities.encryption import generate_secret_key


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--secret_key",
            nargs="?",
            type=int,
            help="Length of key (Default: 50)",
            default=50,
        )
        parser.add_argument(
            "--signing_key",
            nargs="?",
            type=int,
            help="Length of key (Default: 50)",
            default=50,
        )
        parser.add_argument(
            "--encryption_key",
            nargs="?",
            type=int,
            help="Length of key (Default: 100)",
            default=100,
        )

    def handle(self, *args, **options) -> None:
        """
        Generate secret keys for project.
        :param args:
        :param options:
        :return:
        """

        secret_key = generate_secret_key(length=options["secret_key"])
        signing_key = generate_secret_key(length=options["signing_key"])
        encryption_key = Fernet.generate_key()

        self.stdout.write(f"Environment Variable: 'BLOG_SECRET_KEY': {secret_key}")
        self.stdout.write(f"Environment Variable: 'BLOG_SIGNING_KEY': {signing_key}")
        self.stdout.write(f"Environment Variable: 'BLOG_DB_ENCRYPTION_KEY': {encryption_key.decode('utf-8')}")
