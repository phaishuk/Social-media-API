from rest_framework import serializers

from social_network.models import Post, Comment
from user.models import User
from rest_framework.reverse import reverse


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

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "owner",
            "created_at",
            "text",
            "content",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "owner",
            "created_at",
            "post",
            "text",
            "is_updated",
            "content",
        )
