from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from social_network.models import Post
from social_network.serializers import PostSerializer
from user.models import User
from user.serializers import (
    UserSelfSerializer,
    FollowLogicSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    CustomAuthTokenSerializer,
)


class AuthenticationPermissionMixin:
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class CreateUserView(generics.CreateAPIView):
    """
    Here you can create user sending POST request
    """

    serializer_class = UserCreateSerializer


class CreateTokenView(ObtainAuthToken):
    """
    On this endpoint users obtain token.
    Here you can authenticate user sending POST request.
    """

    serializer_class = CustomAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageSelfUserView(
    AuthenticationPermissionMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Endpoint related to managing users self account
    """

    serializer_class = UserSelfSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        instance = serializer.save()
        bio = self.request.data.get("bio")
        picture = self.request.data.get("picture")

        if bio:
            instance.bio = bio
        if picture:
            instance.picture = picture
        instance.save()


class LogoutView(AuthenticationPermissionMixin, APIView):
    """Endpoint for logout. Here user can invalidate self token."""

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully"})


class UserListView(AuthenticationPermissionMixin, generics.ListAPIView):
    """Endpoint for listing users"""

    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.prefetch_related(
            "liked_posts", "following", "followers"
        )

        search_param = self.request.query_params.get("search")
        email_param = self.request.query_params.get("email")

        if search_param:
            queryset = queryset.filter(
                Q(username__icontains=search_param)
                | Q(first_name__icontains=search_param)
                | Q(last_name__icontains=search_param)
            )
        if email_param:
            queryset = queryset.filter(email__icontains=email_param)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description=(
                    "Search parameter. Gives an opportunity "
                    "to search by first name, last name, username. "
                    "Letter case doesn't matter. This will return all "
                    "entities of given param in first names, last names, "
                    "and usernames (ex. ?search=petrovich)"
                ),
                required=False,
                type=str,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(AuthenticationPermissionMixin, generics.RetrieveAPIView):
    """
    Endpoint for representation info about separate user
    """

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.following.filter(id=user_to_follow.id).exists():
            request.user.following.add(user_to_follow)
            return Response(
                {"detail": "You are now following this user."},
                status=status.HTTP_200_OK,
            )

        else:
            request.user.following.remove(user_to_follow)
            return Response(
                {"detail": "You have unfollowed this user."},
                status=status.HTTP_200_OK,
            )


class UserFollowView(AuthenticationPermissionMixin, generics.ListAPIView):
    """
    Endpoint for representation of followers and following users
    """

    serializer_class = FollowLogicSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("id")
        request_path = self.request.path
        if "followers" in request_path:
            return User.objects.filter(following__id=user_id)
        elif "following" in request_path:
            return User.objects.filter(followers__id=user_id)
        else:
            return User.objects.none()


class UserPostListView(AuthenticationPermissionMixin, generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        return Post.objects.filter(owner_id=user_id)


class UserLikedPostsListView(AuthenticationPermissionMixin, generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs["id"])
        return user.liked_posts.all()
