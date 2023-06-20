from django.urls import path, include
from rest_framework import routers

from social_network.views import PostViewSet # , CommentViewSet

router = routers.DefaultRouter()
router.register(prefix="posts", viewset=PostViewSet)
# router.register(prefix="comments", viewset=CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:pk>/like/",
        PostViewSet.as_view({"post": "like"}),
        name="post-like",
    ),
]

app_name = "social_network"
