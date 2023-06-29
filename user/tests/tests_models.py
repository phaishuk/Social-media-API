from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@user.com",
            username="testuser",
            password="testpassword",
        )

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "testuser")


class UserRegistrationTests(TestCase):
    def test_user_registration_requires_email(self):
        username = "test_username"
        password = "password"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="", username=username, password=password
            )

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email="", username=username, password=password
            )
