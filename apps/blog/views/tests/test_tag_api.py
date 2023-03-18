"""
Module for Tag Endpoints.
This module will test all tag Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: March 4th 2023
Version: 1.0
"""
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User, Account
from apps.blog.models import Tag


class TestTagEndpoint(TestCase):
    fixtures = ["tests/account.json", "tests/user.json", "tests/tag.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.account = Account.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_tag_list(self):
        """
        Test get tag list endpoint.
        :return:
        """

        response = self.client.get("/api/tags")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 2, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "0eae88be-03ec-4329-8285-42a378ee3399", "created_date": "2023-03-04T05:27:17.993000Z", "updated_date": "2023-03-04T05:27:17.992000Z", "name": "Python", "description": "Journey with python applications.", "slug": "python"}, {"id": "0393e205-79c0-4281-a392-f29aec8805d0", "created_date": "2023-03-04T05:26:12.717000Z", "updated_date": "2023-03-04T05:26:12.716000Z", "name": "Django", "description": "Django Web Framwork a python library.", "slug": "django"}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_tag(self):
        """
        Test post tag endpoint to create a new tag.
        :return:
        """

        data = {
            "name": "Portfolio Portfolio Portfolio",
            "description": "Personal Portfolio Portfolio Portfolio",
        }

        response = self.client.post("/api/tags", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Portfolio Portfolio Portfolio",
                "description": "Personal Portfolio Portfolio Portfolio",
                "slug": "portfolio-portfolio-portfolio",
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_tag_fail(self):
        """
        Test post tag endpoint to create a new category fail.
        :return:
        """

        data = {"name": "Django", "description": "A A A A"}

        response = self.client.post("/api/tags", data=data)
        expected = {
            "is_error": True,
            "error": {"name": ["tag with this name already exists."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_tag(self):
        """
        Test get tag endpoint to get a tag.
        :return:
        """
        category = Tag.objects.first()

        response = self.client.get(f"/api/tags/{str(category.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Django",
                "description": "Django Web Framwork a python library.",
                "slug": "django",
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_tag_fail(self):
        """
        Test get tag endpoint to get a tag fail.
        :return:
        """

        response = self.client.get(f"/api/tags/239dbd79-8a47-4209-b2b9-f7466fed7ece")
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_tag(self):
        """
        Test put tag endpoint to update a tag.
        :return:
        """
        category = Tag.objects.first()

        data = {
            "description": "Kenneth Carmichael Blog Endpoint",
        }

        response = self.client.put(f"/api/tags/{str(category.id)}", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Django",
                "description": "Kenneth Carmichael Blog Endpoint",
                "slug": "django",
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_tag_fail(self):
        """
        Test put tag endpoint to update a tag fail.
        :return:
        """
        category = Tag.objects.first()

        data = {
            "description": f"{'*'*1000}",
        }

        response = self.client.put(f"/api/tags/{str(category.id)}", data=data)
        expected = {
            "is_error": True,
            "error": {
                "description": ["Ensure this field has no more than 250 characters."]
            },
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_delete_tag(self):
        """
        Test delete tag endpoint to delete a tag.
        :return:
        """
        category = Tag.objects.last()

        response = self.client.delete(f"/api/tags/{str(category.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "tag has been deleted."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
