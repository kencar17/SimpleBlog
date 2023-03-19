"""
Module for Blog Post Endpoints.
This module will test all Blog Post Endpoints.
Authors: Kenneth Carmichael (kencar17)
Date: March 17th 2023
Version: 1.0
"""
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User, Account
from apps.blog.models import BlogPost


class TestBlogPostEndpoint(TestCase):
    fixtures = [
        "tests/account.json",
        "tests/user.json",
        "tests/tag.json",
        "tests/blog.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.account = Account.objects.first()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_get_blog_post_list(self):
        """
        Test get blog post list endpoint.
        :return:
        """

        response = self.client.get("/api/blogs")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "335ce286-c177-4f9a-af25-05c3a94975fb", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "created_date": "2023-03-18T04:23:36.485000Z", "updated_date": "2023-03-18T04:23:36.479000Z", "published_date": null, "status": "DRAFT", "views": 0, "likes": 0, "dislikes": 0, "title": "Exploring the Rich Culture of the Inuvialuit People", "slug": "exploring-the-rich-culture-of-the-inuvialuit-people", "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.", "categories": [], "tags": [], "is_featured": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_blog_post_list_filter_status(self):
        """
        Test get blog post list endpoint.
        :return:
        """

        response = self.client.get("/api/blogs?status=PUBLISHED")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 0, "pages": 0, "current": 0, "previous": null, "next": null, "results": []}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_blog_post_list_filter_is_featured(self):
        """
        Test get blog post list endpoint.
        :return:
        """

        response = self.client.get("/api/blogs?is_featured=True")
        expected = b'{"is_error": false, "error": {}, "content": {"count": 0, "pages": 0, "current": 0, "previous": null, "next": null, "results": []}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_blog_post_list_filter_account(self):
        """
        Test get blog post list endpoint.
        :return:
        """

        response = self.client.get(
            "/api/blogs?account=5b076883-8f47-4372-9089-7f2a9e68f69f"
        )
        expected = b'{"is_error": false, "error": {}, "content": {"count": 1, "pages": 1, "current": 1, "previous": null, "next": null, "results": [{"id": "335ce286-c177-4f9a-af25-05c3a94975fb", "account": "5b076883-8f47-4372-9089-7f2a9e68f69f", "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf", "created_date": "2023-03-18T04:23:36.485000Z", "updated_date": "2023-03-18T04:23:36.479000Z", "published_date": null, "status": "DRAFT", "views": 0, "likes": 0, "dislikes": 0, "title": "Exploring the Rich Culture of the Inuvialuit People", "slug": "exploring-the-rich-culture-of-the-inuvialuit-people", "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.", "categories": [], "tags": [], "is_featured": false}]}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_get_blog_post_list_filter_user(self):
        """
        Test get blog post list endpoint.
        :return:
        """

        response = self.client.get(
            "/api/blogs?account=10c331ef-d067-488e-8c0f-e398d7c8d9d3"
        )
        expected = b'{"is_error": false, "error": {}, "content": {"count": 0, "pages": 0, "current": 0, "previous": null, "next": null, "results": []}}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected)

    def test_create_new_blog_post(self):
        """
        Test post blog post endpoint to create a new blog post.
        :return:
        """

        data = {
            "account": str(Account.objects.first().id),
            "author": str(User.objects.first().id),
            "status": "DRAFT",
            "title": "The Rich Culture of the Inuvialuit People",
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "content": "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        }

        response = self.client.post("/api/blogs", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "author": "10c331ef-d067-488e-8c0f-e398d7c8d9d3",
                "published_date": None,
                "status": "DRAFT",
                "views": 0,
                "likes": 0,
                "dislikes": 0,
                "title": "The Rich Culture of the Inuvialuit People",
                "slug": "the-rich-culture-of-the-inuvialuit-people",
                "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
                "categories": [],
                "tags": [],
                "is_featured": False,
            },
        }

        ret = json.loads(response.content)

        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_create_new_blog_post_fail(self):
        """
        Test post blog post endpoint to create a new blog post fail.
        :return:
        """

        data = {
            "account": str(Account.objects.first().id),
            "author": str(User.objects.first().id),
            "status": "DRAFT",
            "title": "The Rich Culture of the Inuvialuit People" * 10000,
            "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
            "content": "The Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.",
        }

        response = self.client.post("/api/blogs", data=data)
        expected = {
            "is_error": True,
            "error": {"title": ["Ensure this field has no more than 100 characters."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_blog_post(self):
        """
        Test get blog post endpoint to get a blog post.
        :return:
        """
        blog = BlogPost.objects.first()

        response = self.client.get(f"/api/blogs/{str(blog.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf",
                "published_date": None,
                "status": "DRAFT",
                "views": 0,
                "likes": 0,
                "dislikes": 0,
                "title": "Exploring the Rich Culture of the Inuvialuit People",
                "slug": "exploring-the-rich-culture-of-the-inuvialuit-people",
                "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
                "categories": [],
                "tags": [],
                "is_featured": False,
                "content": "Introduction\r\n\r\nThe Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.\r\n\r\nHistory and Settlement\r\n\r\nThe Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.\r\n\r\nLanguage and Dialects\r\n\r\nThe Inuvialuit speak Inuvialuktun, an Inuit language with three main dialects: Siglitun, Uummarmiutun, and Kangiryuarmiutun. Each dialect is spoken in different communities within the ISR, and they all belong to the Eskimo-Aleut language family. The Inuvialuktun language has a complex grammar structure and a rich vocabulary that reflects the traditional way of life of the Inuvialuit people.\r\n\r\nTraditional Practices\r\n\r\nThe Inuvialuit have always had a strong connection to their environment, relying on the land and sea to provide sustenance. Hunting, fishing, and gathering have been essential aspects of their culture, with a focus on marine mammals such as seals, whales, and walruses, as well as caribou and fish species like Arctic char. Their intimate knowledge of the natural world has also informed their understanding of weather patterns, ice conditions, and animal migration.\r\n\r\nInuvialuit culture places great importance on traditional skills and knowledge, including sewing, carving, and tool-making. Women have been responsible for creating functional yet beautiful clothing, such as parkas and mukluks, from animal hides and fur. Men have crafted intricate tools and weapons for hunting and fishing, often from materials such as bone, antler, and ivory.\r\n\r\nStorytelling, drumming, and dancing are also integral aspects of Inuvialuit culture, with oral traditions passed down through generations. These stories often convey lessons, values, and histories, while drumming and dancing provide opportunities for community gatherings and celebrations.\r\n\r\nContemporary Efforts to Preserve Inuvialuit Culture\r\n\r\nIn recent years, the Inuvialuit have faced challenges in preserving their language and traditional way of life due to external factors such as climate change, modernization, and the influence of English. To address these challenges, various initiatives have been established to promote the preservation and revitalization of Inuvialuit culture.\r\n\r\nThe Inuvialuit Final Agreement (IFA), signed in 1984, has been a significant milestone for the Inuvialuit people. The agreement recognized their rights to land, resources, and self-governance, leading to the establishment of the Inuvialuit Settlement Region and the Inuvialuit Regional Corporation. These institutions have played a crucial role in managing land, resources, and economic development for the Inuvialuit people while preserving their culture and way of life.\r\n\r\nLanguage revitalization programs have been implemented to preserve and promote the use of Inuvialuktun. These initiatives include the development of learning materials, language classes, and the incorporation of Inuvialuktun in school curriculums.\r\n\r\nCultural events and festivals, such as the Great Northern Arts Festival and the Inuvialuit Day Celebration, have become crucial platforms for showcasing and celebrating traditional art, music, dance, and storytelling. These events provide opportunities for community members to engage with their heritage and for visitors to learn about and appreciate Inuvialuit culture.\r\n\r\nIn addition, community-based cultural centers and museums, such as the Inuvialuit Cultural Centre and the Tuktoyaktuk Community Museum, work to preserve and display artifacts, traditional clothing, tools, and artwork that reflect the rich history of the Inuvialuit people. These institutions often host workshops, lectures, and demonstrations to educate both community members and visitors about various aspects of Inuvialuit culture and history.\r\n\r\nThe Inuvialuit have also made strides in integrating traditional knowledge with modern technology, such as using GPS tracking for hunting and mapping, and incorporating traditional ecological knowledge into climate change research. These initiatives demonstrate the resilience and adaptability of the Inuvialuit culture, ensuring its relevance and sustainability for future generations.\r\n\r\nConclusion\r\n\r\nThe Inuvialuit people have a rich and diverse cultural heritage that reflects their deep connection to the land, their history, and their traditional way of life. By understanding and appreciating the unique aspects of Inuvialuit culture, we can foster greater respect for their contributions to our shared global heritage. Through continued efforts to preserve their language, traditions, and knowledge, the Inuvialuit people are ensuring that their culture thrives and remains a vital part of Canada's cultural mosaic.",
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_get_blog_post_fail(self):
        """
        Test get blog post endpoint to get a blog post fail.
        :return:
        """

        response = self.client.get(f"/api/blogs/239dbd79-8a47-4209-b2b9-f7466fed7ece")
        expected = {
            "is_error": True,
            "error": {"message": "Not found.", "errors": []},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_blog_post(self):
        """
        Test put blog post endpoint to update a blog post.
        :return:
        """
        category = BlogPost.objects.first()

        data = {
            "title": "Kenneth Carmichael Blog Endpoint",
        }

        response = self.client.put(f"/api/blogs/{str(category.id)}", data=data)
        expected = {
            "is_error": False,
            "error": {},
            "content": {
                "account": "5b076883-8f47-4372-9089-7f2a9e68f69f",
                "author": "60d83116-78f3-43c0-8a7c-948b9b3dcbdf",
                "published_date": None,
                "status": "DRAFT",
                "views": 0,
                "likes": 0,
                "dislikes": 0,
                "title": "Kenneth Carmichael Blog Endpoint",
                "slug": "kenneth-carmichael-blog-endpoint",
                "excerpt": "The Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.",
                "categories": [],
                "tags": [],
                "is_featured": False,
                "content": "Introduction\r\n\r\nThe Inuvialuit people, a group of Inuit indigenous to the western Arctic region of Canada, have a rich cultural heritage that spans thousands of years. Their traditional territory includes the Inuvialuit Settlement Region (ISR), which extends from the Beaufort Sea coast to the interior lands. This blog post aims to explore the Inuvialuit culture, focusing on their history, language, traditional practices, and contemporary efforts to preserve their heritage.\r\n\r\nHistory and Settlement\r\n\r\nThe Inuvialuit are descendants of the ancient Thule people, who migrated from Alaska to the Canadian Arctic around 1000 CE. They settled in the region now known as the Inuvialuit Settlement Region, which includes communities such as Tuktoyaktuk, Paulatuk, Sachs Harbour, Aklavik, and Ulukhaktok. Historically, the Inuvialuit have relied on hunting, fishing, and gathering to sustain their communities, forming deep connections with their environment.\r\n\r\nLanguage and Dialects\r\n\r\nThe Inuvialuit speak Inuvialuktun, an Inuit language with three main dialects: Siglitun, Uummarmiutun, and Kangiryuarmiutun. Each dialect is spoken in different communities within the ISR, and they all belong to the Eskimo-Aleut language family. The Inuvialuktun language has a complex grammar structure and a rich vocabulary that reflects the traditional way of life of the Inuvialuit people.\r\n\r\nTraditional Practices\r\n\r\nThe Inuvialuit have always had a strong connection to their environment, relying on the land and sea to provide sustenance. Hunting, fishing, and gathering have been essential aspects of their culture, with a focus on marine mammals such as seals, whales, and walruses, as well as caribou and fish species like Arctic char. Their intimate knowledge of the natural world has also informed their understanding of weather patterns, ice conditions, and animal migration.\r\n\r\nInuvialuit culture places great importance on traditional skills and knowledge, including sewing, carving, and tool-making. Women have been responsible for creating functional yet beautiful clothing, such as parkas and mukluks, from animal hides and fur. Men have crafted intricate tools and weapons for hunting and fishing, often from materials such as bone, antler, and ivory.\r\n\r\nStorytelling, drumming, and dancing are also integral aspects of Inuvialuit culture, with oral traditions passed down through generations. These stories often convey lessons, values, and histories, while drumming and dancing provide opportunities for community gatherings and celebrations.\r\n\r\nContemporary Efforts to Preserve Inuvialuit Culture\r\n\r\nIn recent years, the Inuvialuit have faced challenges in preserving their language and traditional way of life due to external factors such as climate change, modernization, and the influence of English. To address these challenges, various initiatives have been established to promote the preservation and revitalization of Inuvialuit culture.\r\n\r\nThe Inuvialuit Final Agreement (IFA), signed in 1984, has been a significant milestone for the Inuvialuit people. The agreement recognized their rights to land, resources, and self-governance, leading to the establishment of the Inuvialuit Settlement Region and the Inuvialuit Regional Corporation. These institutions have played a crucial role in managing land, resources, and economic development for the Inuvialuit people while preserving their culture and way of life.\r\n\r\nLanguage revitalization programs have been implemented to preserve and promote the use of Inuvialuktun. These initiatives include the development of learning materials, language classes, and the incorporation of Inuvialuktun in school curriculums.\r\n\r\nCultural events and festivals, such as the Great Northern Arts Festival and the Inuvialuit Day Celebration, have become crucial platforms for showcasing and celebrating traditional art, music, dance, and storytelling. These events provide opportunities for community members to engage with their heritage and for visitors to learn about and appreciate Inuvialuit culture.\r\n\r\nIn addition, community-based cultural centers and museums, such as the Inuvialuit Cultural Centre and the Tuktoyaktuk Community Museum, work to preserve and display artifacts, traditional clothing, tools, and artwork that reflect the rich history of the Inuvialuit people. These institutions often host workshops, lectures, and demonstrations to educate both community members and visitors about various aspects of Inuvialuit culture and history.\r\n\r\nThe Inuvialuit have also made strides in integrating traditional knowledge with modern technology, such as using GPS tracking for hunting and mapping, and incorporating traditional ecological knowledge into climate change research. These initiatives demonstrate the resilience and adaptability of the Inuvialuit culture, ensuring its relevance and sustainability for future generations.\r\n\r\nConclusion\r\n\r\nThe Inuvialuit people have a rich and diverse cultural heritage that reflects their deep connection to the land, their history, and their traditional way of life. By understanding and appreciating the unique aspects of Inuvialuit culture, we can foster greater respect for their contributions to our shared global heritage. Through continued efforts to preserve their language, traditions, and knowledge, the Inuvialuit people are ensuring that their culture thrives and remains a vital part of Canada's cultural mosaic.",
            },
        }

        ret = json.loads(response.content)
        del ret["content"]["id"]
        del ret["content"]["created_date"]
        del ret["content"]["updated_date"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_update_blog_post_fail(self):
        """
        Test put blog post endpoint to update a blog post fail.
        :return:
        """
        category = BlogPost.objects.first()

        data = {
            "title": f"{'*'*10000}",
        }

        response = self.client.put(f"/api/blogs/{str(category.id)}", data=data)
        expected = {
            "is_error": True,
            "error": {"title": ["Ensure this field has no more than 100 characters."]},
            "content": {},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)

    def test_delete_blog_post(self):
        """
        Test delete blog post endpoint to delete a blog post.
        :return:
        """
        blog = BlogPost.objects.last()

        response = self.client.delete(f"/api/blogs/{str(blog.id)}")
        expected = {
            "is_error": False,
            "error": {},
            "content": {"message": "Instance has been deleted."},
        }
        ret = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(ret, expected)
