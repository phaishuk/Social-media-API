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
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "owner",
            "created_at",
            "text",
            "content",
            "liked_by_user",
        )

    def get_liked_by_user(self, obj):
        user = self.context.get("request").user
        return obj.likes.filter(id=user.id).exists()


# class CommentSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ("id", "user", "text", "created_at")
