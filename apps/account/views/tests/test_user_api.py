"""
Module for User Endpoints.
This module will test all user Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: February 11th 2023
Version: 1.0
"""
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User


class TestUserEndpoint(TestCase):
    fixtures = ["tests/account.json", "tests/user.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_user_list(self):
        """
        Test get user list endpoint.
        :return:
        """

        response = self.client.get("/api/users")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 7, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "239dbd79-8a47-4209-b2b9-f7466fed7ece", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar2@kencar.com", "display_name": "", "first_name": "K2", "last_name": "C2", "bio": "", "is_contributor": true, "is_editor": false, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "2c1d04d7-c382-4b19-8e44-62533165f5df", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar3@kencar.com", "display_name": "", "first_name": "K3", "last_name": "C3", "bio": "", "is_contributor": false, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "10c331ef-d067-488e-8c0f-e398d7c8d9d3", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar4@kencar.com", "display_name": "", "first_name": "K4", "last_name": "C4", "bio": "", "is_contributor": false, "is_editor": false, "is_blog_owner": true, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "568e930a-e586-4e41-87bf-5922b34f0f1d", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken3@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": false, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_contributor(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_contributor": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 5, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "239dbd79-8a47-4209-b2b9-f7466fed7ece", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar2@kencar.com", "display_name": "", "first_name": "K2", "last_name": "C2", "bio": "", "is_contributor": true, "is_editor": false, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "568e930a-e586-4e41-87bf-5922b34f0f1d", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken3@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": false, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_editor(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_editor": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 5, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "2c1d04d7-c382-4b19-8e44-62533165f5df", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar3@kencar.com", "display_name": "", "first_name": "K3", "last_name": "C3", "bio": "", "is_contributor": false, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "568e930a-e586-4e41-87bf-5922b34f0f1d", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken3@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": false, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_blog_owner(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_blog_owner": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 5, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "239dbd79-8a47-4209-b2b9-f7466fed7ece", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar2@kencar.com", "display_name": "", "first_name": "K2", "last_name": "C2", "bio": "", "is_contributor": true, "is_editor": false, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "568e930a-e586-4e41-87bf-5922b34f0f1d", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken3@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": false, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_staff(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_staff": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_superuser(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_superuser": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_is_active(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"is_active": True}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 6, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "239dbd79-8a47-4209-b2b9-f7466fed7ece", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar2@kencar.com", "display_name": "", "first_name": "K2", "last_name": "C2", "bio": "", "is_contributor": true, "is_editor": false, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "2c1d04d7-c382-4b19-8e44-62533165f5df", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar3@kencar.com", "display_name": "", "first_name": "K3", "last_name": "C3", "bio": "", "is_contributor": false, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "10c331ef-d067-488e-8c0f-e398d7c8d9d3", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar4@kencar.com", "display_name": "", "first_name": "K4", "last_name": "C4", "bio": "", "is_contributor": false, "is_editor": false, "is_blog_owner": true, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_page_size(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"page_size": 1, "page": 3}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 7, "pages": 7, "current": 3, "previous": "http://testserver/api/users?page=2&page_size=1", "next": "http://testserver/api/users?page=4&page_size=1", "results": [{"id": "2c1d04d7-c382-4b19-8e44-62533165f5df", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar3@kencar.com", "display_name": "", "first_name": "K3", "last_name": "C3", "bio": "", "is_contributor": false, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_user_list_page_size_large(self):
        """
        Test get user list endpoint.
        :return:
        """

        data = {"page_size": 100}

        response = self.client.get("/api/users", data=data)
        expected = b'{"is_error": false, "error": {}, "content": {"count": 7, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kcarmichael@kencar.ca", "display_name": "", "first_name": "Kenneth", "last_name": "Carmichael", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": true, "is_active": true, "is_staff": true, "is_superuser": true}, {"id": "239dbd79-8a47-4209-b2b9-f7466fed7ece", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar2@kencar.com", "display_name": "", "first_name": "K2", "last_name": "C2", "bio": "", "is_contributor": true, "is_editor": false, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "2c1d04d7-c382-4b19-8e44-62533165f5df", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar3@kencar.com", "display_name": "", "first_name": "K3", "last_name": "C3", "bio": "", "is_contributor": false, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "10c331ef-d067-488e-8c0f-e398d7c8d9d3", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "kencar4@kencar.com", "display_name": "", "first_name": "K4", "last_name": "C4", "bio": "", "is_contributor": false, "is_editor": false, "is_blog_owner": true, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "568e930a-e586-4e41-87bf-5922b34f0f1d", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken3@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": false, "is_staff": false, "is_superuser": false}, {"id": "5eb8dcf2-b4fd-4850-9e2c-edc0ff44f3b1", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken1@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}, {"id": "8201fa24-b00b-495c-b72c-591b754c2e62", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "username": "ken2@kencar.ca", "display_name": "", "first_name": "Kenh", "last_name": "Carml", "bio": "Personal Blog of Kenneth Carmichael", "is_contributor": true, "is_editor": true, "is_blog_owner": false, "is_active": true, "is_staff": false, "is_superuser": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_user(self):
        """
        Test post user endpoint to create a new user.
        :return:
        """

        data = {
            "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
            "username": "ken5@kencar.ca",
            "display_name": "",
            "first_name": "Kenh",
            "last_name": "Carml",
            "bio": "Personal Blog of Kenneth Carmichael",
            "is_contributor": True,
            "is_editor": True,
            "is_blog_owner": False,
        }

        response = self.client.post("/api/users", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "username": "ken5@kencar.ca",
                "display_name": "",
                "first_name": "Kenh",
                "last_name": "Carml",
                "bio": "Personal Blog of Kenneth Carmichael",
                "is_contributor": True,
                "is_editor": True,
                "is_blog_owner": False,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        }
        ret = json.loads(response.content)
        del ret["content"]["id"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_user_fail(self):
        """
        Test post user endpoint to create a new user fail.
        :return:
        """

        data = {
            "username": "ken5@kencar.ca",
            "display_name": "",
            "first_name": "Kenh",
            "last_name": "Carml",
            "bio": "Personal Blog of Kenneth Carmichael",
            "is_contributor": True,
            "is_editor": True,
            "is_blog_owner": False,
        }

        response = self.client.post("/api/users", data=data)
        expected = {
            "is_error": True,
            "error": {"account": ["This field is required."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_user(self):
        """
        Test get user endpoint to get a user.
        :return:
        """

        response = self.client.get(f"/api/users/{str(self.user.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "username": "kencar4@kencar.com",
                "display_name": "",
                "first_name": "K4",
                "last_name": "C4",
                "bio": "",
                "is_contributor": False,
                "is_editor": False,
                "is_blog_owner": True,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        }
        ret = json.loads(response.content)
        del ret["content"]["id"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_user_fail(self):
        """
        Test get user endpoint to get a user fail.
        :return:
        """

        response = self.client.get(
            f"/api/users/5b076883-8f47-4372-9089-7f2a9e68f69f"
        )
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_user(self):
        """
        Test put user endpoint to update a user.
        :return:
        """

        data = {
            "display_name": "Carmichael",
            "first_name": "Kenneth",
            "last_name": "Carmichael",
            "bio": "Kenneth Carmichael",
        }

        response = self.client.put(f"/api/users/{str(self.user.id)}", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "username": "kencar4@kencar.com",
                "display_name": "Carmichael",
                "first_name": "Kenneth",
                "last_name": "Carmichael",
                "bio": "Kenneth Carmichael",
                "is_contributor": False,
                "is_editor": False,
                "is_blog_owner": True,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        }
        ret = json.loads(response.content)
        del ret["content"]["id"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_user_fail(self):
        """
        Test put user endpoint to update a user fail.
        :return:
        """

        data = {
            "display_name": "Carmichael",
            "first_name": "Kenneth",
            "last_name": "Carmichael",
            "bio": f"{'*'*1000}",
        }

        response = self.client.put(f"/api/users/{str(self.user.id)}", data=data)
        expected = {
            "is_error": True,
            "error": {"bio": ["Ensure this field has no more than 500 characters."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_delete_user(self):
        """
        Test delete user endpoint to delete a user.
        :return:
        """

        user = User.objects.last()

        response = self.client.delete(f"/api/users/{str(user.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "User has been deactivated."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_user_password_change(self):
        """
        Test user password change
        :return:
        """

        user = User.objects.last()
        data = {
            "password_one": "K3nC@rIs!@wesom3!Too",
            "password_two": "K3nC@rIs!@wesom3!Too",
        }

        response = self.client.put(
            f"/api/users/{str(user.id)}/change_password", data=data
        )
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "User password has been changed."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_user_password_change_404(self):
        """
        Test user password change
        :return:
        """

        data = {
            "password_one": "K3nC@rIs!@wesom3!Too",
            "password_two": "K3nC@rIs!@wesom3!Too",
        }

        response = self.client.put(
            f"/api/users/5b076883-8f47-4372-9089-7f2a9e68f69f/change_password",
            data=data,
        )
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_user_password_change_fail(self):
        """
        Test user password change missing field
        :return:
        """

        user = User.objects.last()
        data = {
            "password_one": "K3nC@rIs!@wesom3!Too",
        }

        response = self.client.put(
            f"/api/users/{str(user.id)}/change_password", data=data
        )
        expected = {
            "is_error": True,
            "error": {"password_two": ["This field is required."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_user_password_change_fail_password_reqs(self):
        """
        Test user password change does not meet requirements
        :return:
        """

        user = User.objects.last()
        data = {
            "password_one": "amanpasswordorsomething",
            "password_two": "amanpasswordorsomething",
        }

        response = self.client.put(
            f"/api/users/{str(user.id)}/change_password", data=data
        )
        expected = {
            "is_error": True,
            "error": {
                "message": "Password Change Failed",
                "errors": {
                    "password": [
                        "The password must contain at least 4 uppercase letter, A-Z.",
                        "The password must contain at least 4 special character: !@#$%^&*;:",
                    ]
                },
            },
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
