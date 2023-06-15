from django.urls import path, include
from rest_framework import routers

from social_network.views import PostViewSet

router = routers.DefaultRouter()

router.register(prefix="posts", viewset=PostViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "social_network"
