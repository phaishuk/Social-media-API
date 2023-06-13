from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
            "password",
            "is_staff",
            "bio",
            "picture",
            "followers",
            "following",
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


class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "picture",
        )
        extra_kwargs = {
            "url": {"view_name": "user:user-detail", "lookup_field": "id"}
        }


class FollowingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "picture",
        )
        extra_kwargs = {
            "url": {"view_name": "user:user-detail", "lookup_field": "id"}
        }
