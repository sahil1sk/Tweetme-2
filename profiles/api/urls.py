from django.urls import path
from .views import (
    user_follow_view,
    profile_detail_api_view,
)

urlpatterns = [
    path('<str:username>/', profile_detail_api_view),   # this help to follow or unfollow the user
    path('<str:username>/follow/', user_follow_view),   # this will return the detail of the profile of the user
]
