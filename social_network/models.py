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
    likes = models.ManyToManyField(to=User)
    is_updated = models.BooleanField(default=False)
    content = models.FileField(
        upload_to="post_content/", blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.title} created at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    is_updated = models.BooleanField(default=False)
    content = models.FileField(
        upload_to="comment_content/", blank=True, null=True
    )

    def __str__(self) -> str:
        return (
            f"Comment by {self.owner.username} "
            f"at {self.created_at} on {self.post}"
        )
