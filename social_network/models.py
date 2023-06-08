from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self) -> str:
        return self.title
