from django.test import TestCase
from django.utils import timezone
from user.models import User
from social_network.models import Post, Like, Comment


class BaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
        )
        self.post = Post.objects.create(
            owner=self.user, title="Test Post", text="This is a test post"
        )
        self.like = Like.objects.create(
            user=self.user, post=self.post, created_at=timezone.now()
        )
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            text="This is a test comment",
            created_at=timezone.now(),
        )


class PostModelTest(BaseModelTest):
    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.text, "This is a test post")
        self.assertEqual(self.post.owner, self.user)
        self.assertIsNotNone(self.post.created_at)

    def test_post_str(self):
        expected_str = f"Test Post created at {self.post.created_at}"
        self.assertEqual(str(self.post), expected_str)


class LikeModelTest(BaseModelTest):
    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.post, self.post)
        self.assertIsNotNone(self.like.created_at)

    def test_like_str(self):
        expected_str = (
            f"{self.user.username} liked Test Post at {self.like.created_at}"
        )
        self.assertEqual(str(self.like), expected_str)


class CommentModelTest(BaseModelTest):
    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertIsNotNone(self.comment.created_at)

    def test_comment_str(self):
        expected_str = f"Comment by {self.user.username} on Test Post at {self.comment.created_at}"
        self.assertEqual(str(self.comment), expected_str)
