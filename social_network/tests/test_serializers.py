import zoneinfo
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from social_network.models import Post, Comment
from social_network.serializers import (
    UserSerializer,
    PostSerializer,
    RestrictedPostSerializer,
    CommentSerializer,
    CommentListSerializer,
)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="userpass"
        )
        self.factory = APIRequestFactory()
        request = self.factory.get("/dummy_url/")
        self.context = {"request": Request(request)}

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user, context=self.context)
        expected_data = {
            "id": self.user.id,
            "username": self.user.username,
            "url": f"http://testserver/api/user/{self.user.id}/",
        }
        self.assertEqual(serializer.data, expected_data)


class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="userpass"
        )
        self.post_title = "Test Post"
        self.post_text = "This is a test post"
        self.post = Post.objects.create(
            owner=self.user, title=self.post_title, text=self.post_text
        )
        self.comment_text = "This is a test comment"
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            text=self.comment_text,
        )
        self.factory = APIRequestFactory()
        request = self.factory.get("/dummy_url/")
        self.context = {"request": Request(request)}
        self.tz = zoneinfo.ZoneInfo(settings.TIME_ZONE)

    def test_post_serializer(self):
        serializer = PostSerializer(instance=self.post, context=self.context)
        expected_data = {
            "id": self.post.id,
            "title": self.post_title,
            "owner": OrderedDict(
                [
                    ("id", self.user.id),
                    ("username", self.user.username),
                    ("url", f"http://testserver/api/user/{self.user.id}/"),
                ]
            ),
            "created_at": self.post.created_at.astimezone(self.tz).isoformat(),
            "text": self.post_text,
            "content": None,
            "liked_by_current_user": False,
            "edited": False,
            "comments": (
                f"http://testserver/api/social_network/posts/"
                f"{self.post.id}/comments/"
            ),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_restricted_post_serializer(self):
        serializer = RestrictedPostSerializer(
            instance=self.post, context=self.context
        )

        expected_data = {
            "title": self.post_title,
            "text": self.post_text,
            "owner": OrderedDict(
                [
                    ("id", self.user.id),
                    ("username", self.user.username),
                    ("url", f"http://testserver/api/user/{self.user.id}/"),
                ]
            ),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_comment_serializer(self):
        serializer = CommentSerializer(
            instance=self.comment, context=self.context
        )
        expected_data = {
            "id": self.comment.id,
            "user": OrderedDict(
                [
                    ("id", self.user.id),
                    ("username", self.user.username),
                    ("url", f"http://testserver/api/user/{self.user.id}/"),
                ]
            ),
            "text": self.comment_text,
            "created_at": self.comment.created_at.astimezone(
                self.tz
            ).isoformat(),
            "edited": False,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_comment_list_serializer(self):
        serializer = CommentListSerializer(
            instance=self.comment, context=self.context
        )
        expected_data = {
            "id": self.comment.id,
            "text": self.comment_text,
            "created_at": self.comment.created_at.astimezone(
                self.tz
            ).isoformat(),
            "edited": False,
        }
        self.assertEqual(serializer.data, expected_data)
