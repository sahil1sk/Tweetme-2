from django.urls import path
from .views import( 
    home_view, 
    tweet_detail_view, 
    tweet_action_view, 
    tweet_list_view, 
    tweet_create_view, 
    tweet_delete_view,
)

urlpatterns = [
    path('', tweet_list_view),                          # this will show the list of the tweets
    path('action/', tweet_action_view),                  # so here we are getting the action
    path('create/', tweet_create_view),                  # this help to create the tweet
    path('<int:tweet_id>/', tweet_detail_view),          # this is for getting the detail of specific tweet
    path('<int:tweet_id>/delete/', tweet_delete_view),   # this help to delete the tweet
]

