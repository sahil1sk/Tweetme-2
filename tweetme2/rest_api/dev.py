from django.contrib.auth import get_user_model
from rest_framework import authentication


User = get_user_model()

class DevAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        qs = User.objects.all()
        user = qs.first()      # qs.order_by("?").first()  ? help to select any random user
        return (user, None)
        