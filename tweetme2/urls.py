"""tweetme2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from tweets.views import( 
    home_view, 
    tweet_detail_view, 
    tweet_action_view, 
    tweet_list_view, 
    tweet_create_view, 
    tweet_delete_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view),
    path('create-tweet', tweet_create_view),                    # this help to create the tweet
    path('tweets', tweet_list_view),                            # this will show the list of the tweets
    path('tweets/<int:tweet_id>', tweet_detail_view),           # this is for getting the detail of specific tweet
    #path('api/tweets/action', tweet_action_view),               # so here we are getting the action
    #path('api/tweets/<int:tweet_id>/delete', tweet_delete_view),# this help to delete the tweet
    path('api/tweets/', include('tweets.urls'))
]

