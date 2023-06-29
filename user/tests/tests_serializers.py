from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory

from user.serializers import (
    BaseUserSerializer,
    UserSelfSerializer,
    UserListSerializer,
    UserDetailSerializer,
    FollowLogicSerializer,
    UserCreateSerializer,
    CustomAuthTokenSerializer,
)


class BaseUserSerializerTest(APITestCase):
    def setUp(self):
        self.test_email = "testuser@user.com"
        self.user = get_user_model().objects.create_user(
            email=self.test_email,
            username="testuser",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.factory = APIRequestFactory()
        request = self.factory.get("/dummy_url/")
        self.context = {"request": Request(request)}

    def test_base_user_serializer(self):
        baseuser_serializer = BaseUserSerializer(
            instance=self.user, context=self.context
        )
        userself_serializer = UserSelfSerializer(
            instance=self.user, context=self.context
        )
        expected_data = {
            "id": self.user.id,
            "email": self.test_email,
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "is_staff": False,
            "bio": None,
            "picture": None,
            "followers_count": 0,
            "following_count": 0,
            "posts_count": 0,
            "followers": f"http://testserver/api/user/{self.user.id}/followers/",
            "following": f"http://testserver/api/user/{self.user.id}/following/",
            "posts": f"http://testserver/api/user/{self.user.id}/posts/",
            "liked_posts": f"http://testserver/api/user/{self.user.id}/liked-posts/",
        }
        self.assertEqual(baseuser_serializer.data, expected_data)
        self.assertEqual(userself_serializer.data, expected_data)

    def test_user_list_serializer(self):
        serializer = UserListSerializer(
            instance=self.user, context=self.context
        )
        expected_data = {
            "id": self.user.id,
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "picture": None,
            "followers_count": 0,
            "following_count": 0,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_user_detail_serializer(self):
        serializer = UserDetailSerializer(
            instance=self.user, context=self.context
        )
        expected_data = {
            "id": self.user.id,
            "email": self.test_email,
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "is_staff": False,
            "bio": None,
            "picture": None,
            "followers_count": 0,
            "following_count": 0,
            "posts_count": 0,
            "followers": f"http://testserver/api/user/{self.user.id}/followers/",
            "following": f"http://testserver/api/user/{self.user.id}/following/",
            "posts": f"http://testserver/api/user/{self.user.id}/posts/",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_follow_logic_serializer(self):
        serializer = FollowLogicSerializer(
            instance=self.user, context=self.context
        )
        expected_data = {
            "id": self.user.id,
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "picture": None,
            "posts": f"http://testserver/api/user/{self.user.id}/posts/",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_user_create_serializer(self):
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword",
            "is_staff": False,
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("newpassword"))
        self.assertFalse(user.is_staff)

    def test_custom_auth_token_serializer_username_label(self):
        serializer = CustomAuthTokenSerializer()
        self.assertEqual(serializer.fields["username"].label, "Email")
