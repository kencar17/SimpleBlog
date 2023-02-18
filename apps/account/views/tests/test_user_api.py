"""
Module for User Endpoints.
This module will test all user Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""

from django.test import TestCase, Client

from rest_framework import status


class TestUserEndpoint(TestCase):

    fixtures = ["tests/account.json", "tests/user.json"]

    def setUp(self):
        self.client = Client()
        self.user = ""
        # self.client.login(username='admintest', password='admintest')

    def test_get_users(self):

        response = self.client.get("/api/account/users")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
