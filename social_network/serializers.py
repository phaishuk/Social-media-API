from rest_framework import serializers
from rest_framework.reverse import reverse

from social_network.models import Post, Comment
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "url")

    def get_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return reverse(
                "user:user-detail", kwargs={"id": obj.id}, request=request
            )
        return None


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    liked_by_current_user = serializers.SerializerMethodField()
    edited = serializers.BooleanField(source="is_updated", read_only=True)
    comments = serializers.HyperlinkedIdentityField(
        view_name="social_network:comment-list",
        lookup_url_kwarg="post_pk",
    )
    scheduled_time = serializers.DateTimeField(
        write_only=True,
        required=False,
    )
    content = serializers.FileField(
        allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "owner",
            "created_at",
            "text",
            "content",
            "liked_by_current_user",
            "edited",
            "comments",
            "scheduled_time",
        )

    def get_liked_by_current_user(self, obj: Post):
        if not isinstance(obj, Post):
            return False
        user = self.context.get("request").user
        return obj.likes.filter(id=user.id).exists()


class RestrictedPostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "text", "owner"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    edited = serializers.BooleanField(source="is_updated", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "text",
            "created_at",
            "edited",
        )


class CommentListSerializer(serializers.ModelSerializer):
    edited = serializers.BooleanField(source="is_updated", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "created_at",
            "edited",
        )
