from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.models import User
from user.serializers import (
    UserSerializer,
    FollowLogicSerializer,
    FollowLogicSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully"})


class UserView(generics.RetrieveAPIView, generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if self.kwargs.get("id"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

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

    def get_queryset(self):
        queryset = User.objects.all()  # TODO maybe prefetch related?

        search_param = self.request.query_params.get("search")
        email_param = self.request.query_params.get("email")

        if search_param:
            queryset = queryset.filter(
                Q(username__icontains=search_param)
                | Q(first_name__icontains=search_param)
                | Q(last_name__icontains=search_param)
            )
        if email_param:
            queryset = queryset.filter(username__icontains=email_param)
        return queryset


class UserFollowView(generics.ListAPIView):
    serializer_class = FollowLogicSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get("id")
        request_path = self.request.path
        if "followers" in request_path:
            return User.objects.filter(following__id=user_id)
        elif "following" in request_path:
            return User.objects.filter(followers__id=user_id)
        else:
            return User.objects.none()
