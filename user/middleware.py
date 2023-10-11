import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware, make_naive, now


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = None
        token = request.META.get("HTTP_AUTHORIZATION")

        if token:
            token = token.split()[-1]
            try:
                decoded_payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                user_id = decoded_payload.get("user_id")
                user = get_user_model().objects.get(pk=user_id)
                user.last_request = make_aware(make_naive(now()))
                user.save()
            except jwt.ExpiredSignatureError:
                pass

        request.user = user

        response = self.get_response(request)
        return response
