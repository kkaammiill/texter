import json

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Article


class ViewArticleTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(body="some body of an article")
        self.client = APIClient()

        self.detail_url = reverse("article-detail", kwargs={"pk": self.article.uuid})
        self.list_url = reverse("article-list")

    def test_acces_article_with_no_token(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "uuid": str(self.article.uuid),
                "body": self.article.body,
                "views_count": 0,
            },
        )

    def test_increment_views_count(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("views_count"), 0)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("views_count"), 1)


class CreateArticleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse("article-list")

    def test_prevent_unauthorized_from_creating(self):
        response = self.client.post(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article(self):
        with self.settings(EDITOR_TOKENS=["ABC"]):
            response = self.client.post(
                self.list_url,
                json.dumps({"body": "article body"}),
                HTTP_AUTHORIZATION="Token ABC",
                content_type="application/json",
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_article = response.json()

        self.assertEqual(created_article.get("body"), "article body")
        self.assertEqual(created_article.get("views_count"), 0)

    def test_body_too_long(self):
        body = "a" * 161
        with self.settings(EDITOR_TOKENS=["ABC"]):
            response = self.client.post(
                self.list_url,
                json.dumps({"body": body}),
                HTTP_AUTHORIZATION="Token ABC",
                content_type="application/json",
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteArticleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.article = Article.objects.create(body="this will be deleted")

        self.detail_url = reverse("article-detail", kwargs={"pk": self.article.uuid})

    def test_prevent_unathorized_from_deleting(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting(self):
        with self.settings(EDITOR_TOKENS=["ABC"]):
            response = self.client.delete(
                self.detail_url,
                HTTP_AUTHORIZATION="Token ABC",
            )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateArticleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.article = Article.objects.create(
            body="this will be updated", views_count=100
        )

        self.detail_url = reverse("article-detail", kwargs={"pk": self.article.uuid})

    def test_prevent_unathorized_from_updating(self):
        response = self.client.post(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating(self):
        with self.settings(EDITOR_TOKENS=["ABC"]):
            response = self.client.put(
                self.detail_url,
                json.dumps({"body": "new body"}),
                HTTP_AUTHORIZATION="Token ABC",
                content_type="application/json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for new content and counter reset
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        article_data = response.json()
        self.assertEqual(article_data.get("body"), "new body")
        self.assertEqual(article_data.get("views_count"), 0)
