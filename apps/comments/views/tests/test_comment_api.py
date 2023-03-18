"""
Module for Comment Endpoints.
This module will test all comment Endpoints.
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
from apps.blog.models import BlogPost
from apps.comments.models import Comment


class TestCommentEndpoint(TestCase):
    fixtures = [
        "tests/account.json",
        "tests/user.json",
        "tests/blog.json",
        "tests/comments.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.account = Account.objects.first()
        self.blog = BlogPost.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_comment_list(self):
        """
        Test get comment list endpoint.
        :return:
        """

        response = self.client.get(
            "/api/comments?blog=335ce286-c177-4f9a-af25-05c3a94975fb"
        )
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "33f2646d-8ef4-45df-aa47-a829ad2f7ba2", "created_date": "2023-03-18T19:23:42.461000Z", "blog": "335ce286-c177-4f9a-af25-05c3a94975fb", "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "parent": null, "content": "AM a comment comment", "children": []}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_comment_list_param_fail(self):
        """
        Test get comment list endpoint.
        :return:
        """

        response = self.client.get("/api/comments")
        expected = b'{"is_error": true, "error": {"message": "Get Failed", "errors": ["\\"blog\\" id is required param."]}, "content": {}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_comment(self):
        """
        Test post comment endpoint to create a new comment.
        :return:
        """

        data = {
            "blog": str(self.blog.id),
            "author": str(self.user.id),
            "content": "Exploring the Rich Culture of the Inuvialuit People",
        }

        response = self.client.post("/api/comments", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "blog": "335ce286-c177-4f9a-af25-05c3a94975fb",
                "author": "10c331ef-d067-488e-8c0f-e398d7c8d9d3",
                "parent": None,
                "content": "Exploring the Rich Culture of the Inuvialuit People",
                "children": [],
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_comment_fail(self):
        """
        Test post comment endpoint to create a new comment fail.
        :return:
        """

        data = {
            "blog": str(self.blog.id),
            "author": str(self.user.id),
            "content": "Exploring the Rich Culture of the Inuvialuit People" * 121,
        }

        response = self.client.post("/api/comments", data=data)
        expected = {
            "is_error": True,
            "error": {
                "content": ["Ensure this field has no more than 250 characters."]
            },
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_comment_user_list(self):
        """
        Test get comment list endpoint.
        :return:
        """

        response = self.client.get(
            "/api/comments/user?user=60d83116-78f3-43c0-8a7c-948b9b3dcbdf"
        )
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "33f2646d-8ef4-45df-aa47-a829ad2f7ba2", "created_date": "2023-03-18T19:23:42.461000Z", "blog": "335ce286-c177-4f9a-af25-05c3a94975fb", "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "parent": null, "content": "AM a comment comment", "children": []}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_comment(self):
        """
        Test get comment endpoint to get a comment.
        :return:
        """
        comment = Comment.objects.first()

        response = self.client.get(f"/api/comments/view/{str(comment.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "blog": "335ce286-c177-4f9a-af25-05c3a94975fb",
                "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf",
                "parent": None,
                "content": "AM a comment comment",
                "children": [],
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_comment_fail(self):
        """
        Test get comment endpoint to get a comment fail.
        :return:
        """

        response = self.client.get(
            f"/api/comments/view/239dbd79-8a47-4209-b2b9-f7466fed7ece"
        )
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_comment(self):
        """
        Test put comment endpoint to update a comment.
        :return:
        """
        comment = Comment.objects.first()

        data = {
            "content": "Kenneth Carmichael Blog Endpoint",
        }

        response = self.client.put(f"/api/comments/view/{str(comment.id)}", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "blog": "335ce286-c177-4f9a-af25-05c3a94975fb",
                "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf",
                "parent": None,
                "content": "Kenneth Carmichael Blog Endpoint",
                "children": [],
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_comment_fail(self):
        """
        Test put comment endpoint to update a comment fail.
        :return:
        """
        comment = Comment.objects.first()

        data = {
            "content": f"{'*'*1000}",
        }

        response = self.client.put(f"/api/comments/view/{str(comment.id)}", data=data)
        expected = {
            "is_error": True,
            "error": {
                "content": ["Ensure this field has no more than 250 characters."]
            },
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_delete_comment(self):
        """
        Test delete comment endpoint to delete a comment.
        :return:
        """
        comment = Comment.objects.first()

        response = self.client.delete(f"/api/comments/view/{str(comment.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "Comment has been deleted."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
