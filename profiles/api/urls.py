from django.urls import path
from .views import (
    profile_detail_api_view,
)

urlpatterns = [
    path('<str:username>/', profile_detail_api_view),   # this help to follow or unfollow the user
    path('<str:username>/follow/', profile_detail_api_view),   # this will return the detail of the profile of the user
]
