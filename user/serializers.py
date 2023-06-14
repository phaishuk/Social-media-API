from rest_framework import serializers
from user.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
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
            "followers",
            "following",
        )

    read_only_fields = ("is_staff",)
    extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


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
            "followers",
            "following",
        )


class UserSelfSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class FollowLogicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "picture",
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
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
