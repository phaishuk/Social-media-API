from django.urls import path

from user.views import (
    CreateUserView,
    CreateTokenView,
    ManageSelfUserView,
    LogoutView,
    UserFollowView,
    UserListView,
    UserDetailView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
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
]
