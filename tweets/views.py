from django.shortcuts import render, redirect
from django.conf import settings # we import this for get allowed hosts

from .models import Tweet
import random
from .forms import TweetForm

# we take the allowed hosts here from settings
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# here we normally show the data
def home_view(request, *args, **kwargs):
    #return HttpResponse("Hello World")
    return render(request, "pages/feed.html", context={}, status=200)



# this function is used to render the list
def tweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")

# this is used to show the detail of each tweet
def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})



