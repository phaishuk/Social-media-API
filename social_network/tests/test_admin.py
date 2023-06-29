from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.urls import reverse

from social_network.admin import PostAdmin, LikeAdmin, CommentAdmin
from social_network.models import Post, Like, Comment


class AdminPanelTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = get_user_model().objects.create_superuser(
            email="test_admin@admin.com",
            username="test_admin",
            password="testadminpassword",
        )
        self.post = Post.objects.create(
            owner=self.user,
            title="Test Post",
            text="This is a test post",
        )
        self.like = Like.objects.create(
            user=self.user,
            post=self.post,
        )
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            text="This is a test comment",
        )
        self.client.login(
            email="test_admin@admin.com",
            password="testadminpassword",
        )

    def test_social_network_models_in_admin_registered(self):
        self.assertIn(Post, admin.site._registry)
        self.assertIn(Comment, admin.site._registry)
        self.assertIn(Like, admin.site._registry)

    def test_post_admin(self):
        post_admin = PostAdmin(model=Post, admin_site=self.site)
        self.assertEqual(
            post_admin.list_display, ("title", "owner", "created_at")
        )
        self.assertEqual(post_admin.list_filter, ("created_at",))
        self.assertEqual(
            post_admin.search_fields, ("title", "owner__username")
        )
        self.assertEqual(post_admin.readonly_fields, ("created_at",))

        url = reverse("admin:social_network_post_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_like_admin(self):
        like_admin = LikeAdmin(model=Like, admin_site=self.site)
        self.assertEqual(
            like_admin.list_display, ("user", "post", "created_at")
        )
        self.assertEqual(like_admin.list_filter, ("created_at",))
        self.assertEqual(
            like_admin.search_fields, ("user__username", "post__title")
        )
        url = reverse("admin:social_network_like_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_comment_admin(self):
        comment_admin = CommentAdmin(model=Comment, admin_site=self.site)
        self.assertEqual(
            comment_admin.list_display, ("user", "post", "created_at", "text")
        )
        self.assertEqual(comment_admin.list_filter, ("created_at",))
        self.assertEqual(
            comment_admin.search_fields, ("user__username", "post__title")
        )
        url = reverse("admin:social_network_comment_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
