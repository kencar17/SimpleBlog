"""
User Manager.
This module will contain custom functionality related to user manager. IE Creation.
Authors: Kenneth Carmichael (kencar17)
Date: February 8th 2023
Version: 1.0
"""
from django.db import models


class UserQuerySet(models.QuerySet):

    def contributors(self):
        return self.filter(is_contributor=True)

    def editors(self):
        return self.filter(is_editor=True)

    def blog_owners(self):
        return self.filter(is_blog_owner=True)
