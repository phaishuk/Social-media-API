from django.urls import path

from user.views import (
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    LogoutView,
    UserView,
    UserFollowersView,
    UserFollowingView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("list/", UserView.as_view(), name="user-list"),
    path("<int:id>/", UserView.as_view(), name="user-detail"),
    path(
        "<int:id>/followers/",
        UserFollowersView.as_view(),
        name="user-followers",
    ),
    path(
        "<int:id>/following/",
        UserFollowingView.as_view(),
        name="user-following",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
