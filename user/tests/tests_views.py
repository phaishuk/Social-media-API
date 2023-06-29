from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social_network.models import Post

TEST_EMAIL = "test@example.com"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password"
TEST_FIRSTNAME = "John"
TEST_LASTNAME = "Doe"


class ManageSelfUserViewTest(APITestCase):
    def setUp(self):
        self.test_new_bio = "New bio"
        self.user = get_user_model().objects.create_user(
            email=TEST_EMAIL,
            username=TEST_EMAIL,
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user:manage")

    def test_retrieve_user_authenticated(self):
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], TEST_EMAIL)
        self.assertEqual(response.data["username"], TEST_EMAIL)

    def test_retrieve_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_authenticated(self):
        url = self.url
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "bio": self.test_new_bio,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Jane")
        self.assertEqual(response.data["last_name"], "Doe")
        self.assertEqual(response.data["bio"], self.test_new_bio)
        # Add more assertions to check other fields

    def test_update_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = self.url
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "bio": self.test_new_bio,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserListViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=TEST_EMAIL,
            username=TEST_EMAIL,
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.client.force_authenticate(user=self.user)

    def test_search_users_by_name(self):
        url = reverse("user:user-list")
        response = self.client.get(url, {"search": TEST_EMAIL})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_users_by_email_authenticated(self):
        url = reverse("user:user-list")
        response = self.client.get(url, {"email": TEST_EMAIL})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserDetailViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=TEST_EMAIL,
            username=TEST_EMAIL,
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.user_to_follow = get_user_model().objects.create_user(
            email="user2@example.com",
            username="user2",
            password="password",
            first_name="Jane",
            last_name="Smith",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse(
            "user:user-detail", kwargs={"id": self.user_to_follow.id}
        )

    def test_get_user_detail_authenticated(self):
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_user_authenticated(self):
        url = self.url
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"], "You are now following this user."
        )

    def test_follow_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = self.url
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_self_user(self):
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "You cannot follow yourself."
        )

    def test_unfollow_user_authenticated(self):
        self.user.following.add(self.user_to_follow)
        url = self.url
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"], "You have unfollowed this user."
        )

    def test_unfollow_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        self.user.following.add(self.user_to_follow)
        url = self.url
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BaseUserPostsTest(APITestCase):
    def setUp(self):
        self.user = self.create_test_user()
        self.post1 = Post.objects.create(
            owner=self.user, title="Test title 1", text="Test text 1"
        )
        self.post2 = Post.objects.create(
            owner=self.user, title="Test title 2", text="Test text 2"
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def create_test_user():
        return get_user_model().objects.create_user(
            email=TEST_EMAIL,
            username=TEST_EMAIL,
            password="password",
            first_name="John",
            last_name="Doe",
        )


class UserPostListViewTest(BaseUserPostsTest):
    def test_get_user_posts_authenticated(self):
        url = reverse("user:user-posts", kwargs={"id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check the response data and structure

    def test_get_user_posts_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("user:user-posts", kwargs={"id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLikedPostsListViewTest(BaseUserPostsTest):
    def setUp(self):
        super().setUp()
        self.user.liked_posts.add(self.post1)

    def test_get_user_liked_posts_authenticated(self):
        url = reverse("user:user-liked-posts", kwargs={"id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_liked_posts_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("user:user-liked-posts", kwargs={"id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
