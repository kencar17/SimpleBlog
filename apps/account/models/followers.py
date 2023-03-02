"""
Account database Model.
This module will contain functions and fields for Account Model.
Authors: Kenneth Carmichael (kencar17)
Date: January 29th 2023
Version: 1.0
"""
import uuid

from django.db.models import UUIDField, ForeignKey, PROTECT

from apps.account.models import Account
from apps.common.models.base_model import BaseTable


# TODO: Account Followers
# TODO: Account Following
# TODO: Encrypting and Decrypting database fields


class Followers(BaseTable):
    """
    Account Model
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    follower = ForeignKey(
        Account, on_delete=PROTECT, help_text="The user who is following an account."
    )
    followed = ForeignKey(
        Account,
        on_delete=PROTECT,
        help_text="The user who is being followed by an account",
    )

    def __str__(self):
        return f"{self.follower} is following {self.followed}"
