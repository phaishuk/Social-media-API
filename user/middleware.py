import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")

        if token:
            token = token.split()[-1]
            try:
                decoded_payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                user_id = decoded_payload.get("user_id")
                user = get_user_model().objects.get(pk=user_id)
                user.last_request = timezone.now()
                user.save()
            except jwt.ExpiredSignatureError:
                pass

        response = self.get_response(request)
        return response
