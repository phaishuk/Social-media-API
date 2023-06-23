from pathlib import Path

from celery import shared_task

from social_network.models import Post
from user.models import User


@shared_task
def create_post(owner_id, title, text, content_path=None):
    owner = User.objects.get(id=owner_id)
    content = Path(content_path) if content_path else None
    Post.objects.create(
        owner=owner,
        title=title,
        text=text,
        content=content,
    )
