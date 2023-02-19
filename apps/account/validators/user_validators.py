"""
User Validators.
This module will contain user validators.
Authors: Kenneth Carmichael (kencar17)
Date: February 10th 2023
Version: 1.0
"""

import re
from django.core.exceptions import ValidationError


class UppercaseValidator(object):
    """
    The password must contain at least 1 uppercase letter, A-Z.
    """

    def validate(self, password, user=None):
        """

        :param password:
        :param user:
        :return:
        """
        chars = re.findall("[A-Z]", password)

        if not re.findall("[A-Z]", password):
            raise ValidationError(
                "The password must contain at least 4 uppercase letter, A-Z.",
                code="password_no_upper",
            )

        if len(chars) < 4:
            raise ValidationError(
                "The password must contain at least 4 uppercase letter, A-Z.",
                code="password_no_upper",
            )

    def get_help_text(self):
        """

        :return:
        """
        return "Your password must contain at least 4 uppercase letter, A-Z."


class SpecialCharValidator(object):
    """
    The password must contain at least 1 special character!@#$%^&*;:
    """

    def validate(self, password, user=None):
        chars = re.findall("[!@#$%^&*;:]", password)

        if not chars:
            raise ValidationError(
                "The password must contain at least 4 special character: !@#$%^&*;:",
                code="password_no_symbol",
            )

        if len(chars) < 4:
            raise ValidationError(
                "The password must contain at least 4 special character: !@#$%^&*;:",
                code="password_no_symbol",
            )

    def get_help_text(self):
        return "Your password must contain at least 4 special character: !@#$%^&*;:"
