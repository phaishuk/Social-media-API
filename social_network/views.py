from datetime import datetime

from django.db.models import Q
from django.utils.timezone import make_aware
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_network.models import Post, Comment
from social_network.permissions import (
    IsOwnerOrAdminOrReadOnly,
    IsCommentOwnerOrPostOwnerOrAdminOrGetMethod,
)
from social_network.serializers import (
    PostSerializer,
    CommentSerializer,
    RestrictedPostSerializer,
)
from tasks.post_creation_task import create_post


class PostViewSet(viewsets.ModelViewSet):
    """
    Gives an opportunity to maintain Post functionality depending on the request.
    """

    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return PostSerializer
        return RestrictedPostSerializer

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

    @action(
        detail=True, methods=["post"], permission_classes=(IsAuthenticated,)
    )
    def like(self, request, pk=None):
        """
        Sending POST request you can put a like for post
        """
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return Response({"liked": liked}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Post.objects.prefetch_related("owner")

        search_param = self.request.query_params.get("search")

        if search_param:
            queryset = queryset.filter(
                Q(title__icontains=search_param)
                | Q(text__icontains=search_param)
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description=(
                    "Search parameter. Gives an opportunity "
                    "to search by post's title or text. "
                    "Letter case doesn't matter. This will return all "
                    "entities of given param in titles and texts. "
                    "(ex. ?search=OREO)"
                ),
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Gives an opportunity to maintain Comment functionality depending on the request.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCommentOwnerOrPostOwnerOrAdminOrGetMethod,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)
