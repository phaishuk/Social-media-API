from django.db import models

from user.models import User


class Post(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    likes = models.ManyToManyField(
        User, through="Like", related_name="liked_posts"
    )
    is_updated = models.BooleanField(default=False)
    content = models.FileField(
        upload_to="post_content/", blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.title} created at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} liked "
            f"{self.post.title} at {self.created_at}"
        )


class Comment(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Comment by {self.user.username} on "
            f"{self.post.title} at {self.created_at}"
        )
