"""
Module for Category Endpoints.
This module will test all category Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: March 3rd 2023
Version: 1.0
"""
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User, Account
from apps.blog.models import Category


class TestCategoryEndpoint(TestCase):
    fixtures = ["tests/account.json", "tests/user.json", "tests/category.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.account = Account.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_category_list(self):
        """
        Test get category list endpoint.
        :return:
        """

        response = self.client.get("/api/categories")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 3, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "869925bc-f9ab-4974-a849-27d3b5fdb74a", "created_date": "2023-03-04T05:31:16.680000Z", "updated_date": "2023-03-04T05:31:16.675000Z", "name": "Portfolio", "description": "Personal Portfolio", "slug": "portfolio", "parent": {"id": "0eae88be-03ec-4329-8285-42a378ee3399", "name": "Python"}}, {"id": "0eae88be-03ec-4329-8285-42a378ee3399", "created_date": "2023-03-04T05:27:17.993000Z", "updated_date": "2023-03-04T05:27:17.992000Z", "name": "Python", "description": "Journey with python applications.", "slug": "python", "parent": null}, {"id": "0393e205-79c0-4281-a392-f29aec8805d0", "created_date": "2023-03-04T05:26:12.717000Z", "updated_date": "2023-03-04T05:26:12.716000Z", "name": "Django", "description": "Django Web Framwork a python library.", "slug": "django", "parent": null}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_category_list_param(self):
        """
        Test get category list endpoint.
        :return:
        """

        response = self.client.get(
            "/api/categories?category=0eae88be-03ec-4329-8285-42a378ee3399"
        )
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "869925bc-f9ab-4974-a849-27d3b5fdb74a", "created_date": "2023-03-04T05:31:16.680000Z", "updated_date": "2023-03-04T05:31:16.675000Z", "name": "Portfolio", "description": "Personal Portfolio", "slug": "portfolio", "parent": {"id": "0eae88be-03ec-4329-8285-42a378ee3399", "name": "Python"}}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_category(self):
        """
        Test post category endpoint to create a new category.
        :return:
        """

        data = {
            "name": "Portfolio Portfolio Portfolio",
            "description": "Personal Portfolio Portfolio Portfolio",
        }

        response = self.client.post("/api/categories", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Portfolio Portfolio Portfolio",
                "description": "Personal Portfolio Portfolio Portfolio",
                "slug": "portfolio-portfolio-portfolio",
                "parent": None,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_category_fail(self):
        """
        Test post category endpoint to create a new category fail.
        :return:
        """

        data = {"name": "Django", "description": "A A A A"}

        response = self.client.post("/api/categories", data=data)
        expected = {
            "is_error": True,
            "error": {"name": ["category with this name already exists."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_category(self):
        """
        Test get category endpoint to get a category.
        :return:
        """
        category = Category.objects.first()

        response = self.client.get(f"/api/categories/{str(category.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Django",
                "description": "Django Web Framwork a python library.",
                "slug": "django",
                "parent": None,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_category_fail(self):
        """
        Test get category endpoint to get a category fail.
        :return:
        """

        response = self.client.get(
            f"/api/categories/239dbd79-8a47-4209-b2b9-f7466fed7ece"
        )
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_category(self):
        """
        Test put category endpoint to update a category.
        :return:
        """
        category = Category.objects.first()

        data = {
            "description": "Kenneth Carmichael Blog Endpoint",
        }

        response = self.client.put(f"/api/categories/{str(category.id)}", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "name": "Django",
                "description": "Kenneth Carmichael Blog Endpoint",
                "slug": "django",
                "parent": None,
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_category_fail(self):
        """
        Test put category endpoint to update a category fail.
        :return:
        """
        category = Category.objects.first()

        data = {
            "description": f"{'*'*1000}",
        }

        response = self.client.put(f"/api/categories/{str(category.id)}", data=data)
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

    def test_delete_category(self):
        """
        Test delete category endpoint to delete a category.
        :return:
        """
        category = Category.objects.last()

        response = self.client.delete(f"/api/categories/{str(category.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "Instance has been deleted."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
