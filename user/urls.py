from django.urls import path

from user.views import (
    CreateUserView,
    ManageSelfUserView,
    UserFollowView,
    UserListView,
    UserDetailView,
    UserPostListView,
    UserLikedPostsListView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageSelfUserView.as_view(), name="manage"),
    path("list/", UserListView.as_view(), name="user-list"),
    path("<int:id>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "<int:id>/followers/",
        UserFollowView.as_view(),
        name="user-followers",
    ),
    path(
        "<int:id>/following/",
        UserFollowView.as_view(),
        name="user-following",
    ),
    path("<int:id>/posts/", UserPostListView.as_view(), name="user-posts"),
    path(
        "<int:id>/liked-posts/",
        UserLikedPostsListView.as_view(),
        name="user-liked-posts",
    ),
]
