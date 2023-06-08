from django.contrib.auth.models import User, Group
from rest_framework import serializers

from social_network.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "text")
