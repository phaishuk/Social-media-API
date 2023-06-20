from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_network.models import Post, Comment
from social_network.permissions import IsOwnerOrReadOnly
from social_network.serializers import (
    PostSerializer,
    CommentSerializer,
    CommentListSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user, is_updated=True)

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
    queryset = Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self, serializer=CommentListSerializer):
        if self.action == "list":
            return serializer
        return CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user, is_updated=True)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user != request.user:
            return Response(
                {"error": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            comment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

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
