"""
Module for Account Endpoints.
This module will test all account Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: February 28th 2023
Version: 1.0
"""
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import Account, User


class TestAccountEndpoint(TestCase):
    fixtures = ["tests/account.json", "tests/user.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.account = Account.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_account_list(self):
        """
        Test get account list endpoint.
        :return:
        """

        response = self.client.get("/api/account/accounts")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "5b076883-8f47-4372-9089-7f2a9e68f69f", "created_date": "2023-02-04T07:52:25.141000Z", "account_name": "New Star Blog", "bio": "Personal Blog", "contact_email": "kc@kencar.ca", "website_link": "", "facebook_link": "", "instagram_link": "", "twitter_link": "", "tiktok_link": "", "linkedin_link": "", "snapchat_link": "", "youtube_link": "", "twitch_link": "", "is_active": true}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_account(self):
        """
        Test post account endpoint to create a new account.
        :return:
        """

        data = {
            "account_name": "KENCARTWO",
            "bio": "",
            "contact_email": "kenccar8@kenccar.com",
        }

        response = self.client.post("/api/account/accounts", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account_name": "KENCARTWO",
                "bio": "Am a blog for KENCARTWO",
                "contact_email": "kenccar8@kenccar.com",
                "website_link": None,
                "facebook_link": None,
                "instagram_link": None,
                "twitter_link": None,
                "tiktok_link": None,
                "linkedin_link": None,
                "snapchat_link": None,
                "youtube_link": None,
                "twitch_link": None,
                "is_active": True,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_account_fail(self):
        """
        Test post account endpoint to create a new account fail.
        :return:
        """

        data = {
            "account_name": "New Star Blog",
            "bio": "",
            "contact_email": "kenccar8@kenccar.com",
        }

        response = self.client.post("/api/account/accounts", data=data)
        expected = {
            "is_error": True,
            "error": {
                "account_name": ["account with this account name already exists."]
            },
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_account(self):
        """
        Test get account endpoint to get a account.
        :return:
        """

        response = self.client.get(f"/api/account/accounts/{str(self.account.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "created_date": "2023-02-04T07:52:25.141000Z",
                "account_name": "New Star Blog",
                "bio": "Personal Blog",
                "contact_email": "kc@kencar.ca",
                "website_link": "",
                "facebook_link": "",
                "instagram_link": "",
                "twitter_link": "",
                "tiktok_link": "",
                "linkedin_link": "",
                "snapchat_link": "",
                "youtube_link": "",
                "twitch_link": "",
                "is_active": True,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_account_fail(self):
        """
        Test get account endpoint to get a account fail.
        :return:
        """

        response = self.client.get(
            f"/api/account/accounts/239dbd79-8a47-4209-b2b9-f7466fed7ece"
        )
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_account(self):
        """
        Test put account endpoint to update a account.
        :return:
        """

        data = {
            "bio": "Kenneth Carmichael Blog Endpoint",
        }

        response = self.client.put(
            f"/api/account/accounts/{str(self.account.id)}", data=data
        )
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "id": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "account_name": "New Star Blog",
                "bio": "Kenneth Carmichael Blog Endpoint",
                "contact_email": "kc@kencar.ca",
                "website_link": "",
                "facebook_link": "",
                "instagram_link": "",
                "twitter_link": "",
                "tiktok_link": "",
                "linkedin_link": "",
                "snapchat_link": "",
                "youtube_link": "",
                "twitch_link": "",
                "is_active": True,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["created_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_account_fail(self):
        """
        Test put account endpoint to update a account fail.
        :return:
        """

        data = {
            "bio": f"{'*'*1000}",
        }

        response = self.client.put(
            f"/api/account/accounts/{str(self.account.id)}", data=data
        )
        expected = {
            "is_error": True,
            "error": {"bio": ["Ensure this field has no more than 500 characters."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_delete_account(self):
        """
        Test delete account endpoint to delete a account.
        :return:
        """

        response = self.client.delete(f"/api/account/accounts/{str(self.account.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "Account has been deactivated."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
