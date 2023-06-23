from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_network.models import Post, Comment
from social_network.permissions import IsOwnerOrReadOnly
from social_network.serializers import (
    PostSerializer,
    CommentSerializer,
)
from tasks.post_creation_task import create_post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        scheduled_time = self.request.data.get("scheduled_time")
        if scheduled_time:
            try:
                scheduled_datetime = datetime.fromisoformat(scheduled_time)
                if scheduled_datetime <= datetime.now():
                    raise ValidationError(
                        "Scheduled time must be in the future."
                    )
            except (TypeError, ValueError):
                raise ValidationError("Invalid scheduled time format.")

            scheduled_datetime = make_aware(scheduled_datetime)
            post_data = serializer.validated_data
            create_post.apply_async(
                args=[
                    self.request.user.id,
                    post_data["title"],
                    post_data["text"],
                ],
                kwargs={"content_path": self.request.FILES.get("content")},
                eta=scheduled_datetime,
            )
        else:
            serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return Response({"liked": liked}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user != request.user:
            return Response(
                {"error": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["owner"] = comment.owner_id
        serializer = self.get_serializer(
            comment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user, is_updated=True)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user != request.user and comment.post.owner != request.user:
            return Response(
                {
                    "error": "You do not have permission to delete this comment."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
