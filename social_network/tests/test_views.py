from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from social_network.models import Post, Comment


class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.test_new_title = "New Post"
        self.test_updated_title = "Updated Post"
        self.test_title_name = "Test Post"
        self.test_post_text = "This is a test post"
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@admin.com",
            username="testuser",
            password="testpassword",
        )
        self.admin = get_user_model().objects.create_superuser(
            email="testadmin@admin.com",
            username="admin",
            password="adminpassword",
        )
        self.post = Post.objects.create(
            owner=self.user,
            title=self.test_title_name,
            text=self.test_post_text,
        )
        self.url = reverse("social_network:post-list")
        self.detail_url = reverse(
            "social_network:post-detail", args=[self.post.id]
        )

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": self.test_new_title, "text": "This is a new post"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Post.objects.latest("created_at").title, self.test_new_title
        )

    def test_create_post_unauthenticated(self):
        data = {"title": self.test_new_title, "text": "This is a new post"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_owner(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url
        data = {
            "title": self.test_updated_title,
            "text": "This post has been updated",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, self.test_updated_title)

    def test_update_post_unauthenticated(self):
        url = self.detail_url
        data = {
            "title": self.test_updated_title,
            "text": "This post has been updated",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, self.test_updated_title)

    def test_delete_post_owner(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = self.detail_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_unauthenticated(self):
        url = self.detail_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_like_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("social_network:post-like", args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["liked"], True)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["liked"], False)

    def test_like_post_unauthenticated(self):
        url = reverse("social_network:post-like", args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_posts(self):
        url = f"{self.url}?search=tEst"
        response = self.client.get(url)
        expected_data = [
            OrderedDict(
                [
                    ("title", self.test_title_name),
                    ("text", self.test_post_text),
                    (
                        "owner",
                        OrderedDict(
                            [
                                ("id", self.user.id),
                                ("username", self.user.username),
                                ("url", "http://testserver/api/user/5/"),
                            ]
                        ),
                    ),
                ]
            )
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, expected_data)


class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.test_new_comment = "New comment"
        self.test_updated_comment = "Updated comment"
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="testadmin@admin.com",
            username="testadmin",
            password="adminpassword",
        )
        self.user1 = get_user_model().objects.create_user(
            email="testuser1@test.com",
            username="testuser1",
            password="user1password",
        )
        self.user2 = get_user_model().objects.create_user(
            email="testuser2@test.com",
            username="testuser2",
            password="user2password",
        )
        self.post = Post.objects.create(
            owner=self.user1,
            title="Test Post",
            text="This is a test post in comment",
        )
        self.comment = Comment.objects.create(
            user=self.user2, post=self.post, text="Test comment"
        )
        self.url = reverse("social_network:comment-list", args=[self.post.id])
        self.detail_url = reverse(
            "social_network:comment-detail",
            args=[self.post.id, self.comment.id],
        )

    def test_list_comments(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        data = {"text": self.test_new_comment}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_unauthenticated(self):
        data = {"text": self.test_new_comment}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_comment(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Test comment")

    def test_update_comment_owner(self):
        self.client.force_authenticate(user=self.user2)
        data = {"text": self.test_updated_comment}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, self.test_updated_comment)

    def test_update_comment_unauthenticated(self):
        data = {"text": self.test_updated_comment}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.text, self.test_updated_comment)

    def test_delete_comment_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_post_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_update_comment_permissions(self):
        test_cases = [
            (self.admin, status.HTTP_403_FORBIDDEN),
            (self.user1, status.HTTP_403_FORBIDDEN),
        ]

        data = {"text": self.test_updated_comment}

        for user, expected_status in test_cases:
            self.client.force_authenticate(user=user)
            response1 = self.client.patch(self.detail_url, data)
            response2 = self.client.put(self.detail_url, data)
            self.assertEqual(response1.status_code, expected_status)
            self.assertEqual(response2.status_code, expected_status)
            self.comment.refresh_from_db()
            self.assertNotEqual(self.comment.text, self.test_updated_comment)
