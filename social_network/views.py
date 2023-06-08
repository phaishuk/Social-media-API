from rest_framework import viewsets

from social_network.models import Post
from social_network.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
