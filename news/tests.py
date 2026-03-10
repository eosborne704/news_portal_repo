from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from news.models import CustomUser, Article, Publisher, Journalist, Newsletter
from unittest.mock import patch


class ArticleAPITests(APITestCase):
    """
    Testing the Article API
    """

    def setUp(self):
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.editor = CustomUser.objects.create_user(
            username="editor", email="editor@test.com", password="pass", role="editor"
        )
        self.journalist_user = CustomUser.objects.create_user(
            username="journalist",
            email="journalist@test.com",
            password="pass",
            role="journalist",
        )
        self.journalist = Journalist.objects.create(
            user=self.journalist_user, publisher=self.publisher
        )
        self.reader = CustomUser.objects.create_user(
            username="reader", email="reader@test.com", password="pass", role="reader"
        )
        self.reader.subscriptions_publishers.add(self.publisher)
        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            approved=True,
            author=self.journalist,
            publisher=self.publisher,
        )

    def test_reader_can_get_subscribed_articles(self):
        """
        Ensures reader only recieves articles they
        are subscribed
        """
        self.client.force_authenticate(user=self.reader)
        url = reverse("article-subscribed")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(a["id"] == self.article.id for a in response.data))

    def test_journalist_can_create_article(self):
        """
        Ensures journalists can write articles
        """
        self.client.force_authenticate(user=self.journalist_user)
        url = reverse("article-list")
        data = {
            "title": "New Article",
            "content": "New Content",
            "author": self.journalist.id,
            "publisher": self.publisher.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_editor_can_approve_article(self):
        """
        Editor can approve article successfully.
        Checks approval endpoint and status.
        """
        self.client.force_authenticate(user=self.editor)
        url = reverse("article-approve", args=[self.article.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)

    def test_editor_can_delete_article(self):
        """
        Ensures an editor can delete articles
        """
        self.client.force_authenticate(user=self.editor)
        url = reverse("article-detail", args=[self.article.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_newsletter_behavior(self):
        """
        Ensures newsletter links function
        properly
        """
        newsletter = Newsletter.objects.create(
            title="NL", description="desc", author=self.journalist
        )
        newsletter.articles.add(self.article)
        self.assertIn(self.article, newsletter.articles.all())

    def test_unauthenticated_access_denied(self):
        """
        Tests enforcement of denying
        unauthorized users
        """
        url = reverse("article-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reader_cannot_create_article(self):
        """
        Makes sure a reader cannot write articles
        """
        self.client.force_authenticate(user=self.reader)
        url = reverse("article-list")
        data = {
            "title": "Should Fail",
            "content": "Nope",
            "author": self.journalist.id,
            "publisher": self.publisher.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journalist_cannot_approve_article(self):
        """
        Makes sure a journalist cannot approve
        an article, only an editor
        """
        self.client.force_authenticate(user=self.journalist_user)
        url = reverse("article-approve", args=[self.article.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_cannot_delete_article(self):
        """
        Ensures article deletion is not
        possible for reader
        """
        self.client.force_authenticate(user=self.reader)
        url = reverse("article-detail", args=[self.article.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_article_id_returns_404(self):
        """
        Checks not found status for ID.
        """
        self.client.force_authenticate(user=self.editor)
        url = reverse("article-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signal_email_sent_on_approve(self):
        """
        Email sent when article approved.
        Mocks signal for email sending.
        """
        with patch("news.api_views.send_article_approved_email") as mock_send_mail:
            self.client.force_authenticate(user=self.editor)
            url = reverse("article-approve", args=[self.article.id])
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(mock_send_mail.called)


class NewsApiTest(TestCase):
    """
    Article creation test
    """

    def test_article_creation(self):
        pass
