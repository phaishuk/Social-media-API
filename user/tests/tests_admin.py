from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import User


class UserAdminPanelTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email="testadmin@admin.com",
            username="testadmin",
            password="adminpassword",
        )
        self.client.force_login(self.admin_user)

    def test_user_model_admin_registered(self):
        self.assertIn(User, admin.site._registry)

    def test_list_display(self):
        model_admin = admin.site._registry[User]
        self.assertEqual(
            list(model_admin.get_list_display(None)),
            ["email", "first_name", "last_name", "is_staff"],
        )

    def test_search_fields(self):
        model_admin = admin.site._registry[User]
        self.assertEqual(
            list(model_admin.get_search_fields(None)),
            ["email", "first_name", "last_name"],
        )

    def test_ordering(self):
        model_admin = admin.site._registry[User]
        self.assertEqual(model_admin.get_ordering(None), ("email",))
