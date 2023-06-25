from collections import OrderedDict

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from user.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers = serializers.HyperlinkedIdentityField(
        view_name="user:user-followers",
        lookup_field="id",
        lookup_url_kwarg="id",
    )
    following = serializers.HyperlinkedIdentityField(
        view_name="user:user-following",
        lookup_field="id",
        lookup_url_kwarg="id",
    )
    posts = serializers.HyperlinkedIdentityField(
        view_name="user:user-posts",
        lookup_field="id",
        lookup_url_kwarg="id",
    )
    liked_posts = serializers.HyperlinkedIdentityField(
        view_name="user:user-liked-posts",
        lookup_field="id",
        lookup_url_kwarg="id",
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "bio",
            "picture",
            "followers_count",
            "following_count",
            "posts_count",
            "followers",
            "following",
            "posts",
            "liked_posts",
        )

        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_count(self, obj):
        return obj.posts.count()


class UserSelfSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "picture",
            "followers_count",
            "following_count",
        )


class UserDetailSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "bio",
            "picture",
            "followers_count",
            "following_count",
            "posts_count",
            "followers",
            "following",
            "posts",
        )


class FollowLogicSerializer(
    serializers.HyperlinkedModelSerializer, BaseUserSerializer
):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "picture",
            "posts",
        )
        extra_kwargs = {
            "url": {"view_name": "user:user-detail", "lookup_field": "id"}
        }


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "password",
            "is_staff",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = self.fields.pop("username")
        self.fields["email"].label = "Email"
        self.fields = OrderedDict(
            [
                ("email", self.fields["email"]),
                ("password", self.fields["password"]),
            ]
        )
