"""
Base database Model.
This module will contain functions and fields for Base Model for common functionality.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""

from cryptography.fernet import Fernet
from django.db.models import Model

from SimpleBlog.settings import DB_ENCRYPTION_KEY


class BaseTable(Model):
    class Meta:
        abstract = True

    def set_values(self, pairs: dict) -> list:
        ret = []

        for key, value in pairs.items():
            if not hasattr(self, key):
                continue
            setattr(self, key, value)
            ret.append(key)

        return ret

    @staticmethod
    def encrypt(value: str) -> str:
        """
        stored database token and return actual value
        Encrypt value to be stored as a token into the database
        :param value: str value to be encrypted
        :return: Encrypted Value
        """

        f = Fernet(DB_ENCRYPTION_KEY.encode())
        token = f.encrypt(value.encode())

        return token.decode("utf-8")

    @staticmethod
    def decrypt(token: str) -> str:
        """
        Decrypt stored database token and return actual value
        :param token: Token to be decrypted
        :return: Decrypted Value
        """
        f = Fernet(DB_ENCRYPTION_KEY.encode())
        value = f.decrypt(token.encode())

        return value.decode("utf-8")

    # Override
    def save(self, *args, **kwargs) -> None:
        self.clean_fields()
        super().save(*args, **kwargs)
