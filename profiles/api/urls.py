from django.urls import path
from .views import user_follow_view

urlpatterns = [
    path('<str:username>/follow/', user_follow_view),   # this help to follow or unfollow the user
]
