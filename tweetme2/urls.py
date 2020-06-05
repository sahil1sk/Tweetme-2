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
from django.urls import path, re_path, include  # re_path is regular expression path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # this will help to render every template which we want

from accounts.views import (
    login_view,
    logout_view,
    register_view
)

from tweets.views import( 
    home_view,
    tweets_list_view,
    tweets_detail_view,
)

urlpatterns = [
    path('', home_view),                            # this will show our tweet and to whom we follow tweets if we authenticated otherwise it will show global tweet
    path('admin/', admin.site.urls),
    path('global/', tweets_list_view),              # this is for showing all the tweets             
    path('<int:tweet_id>', tweets_detail_view),             # this is for showing the detail of the tweet 
    re_path(r'profiles?/', include('profiles.urls')),          # prfiles? s is optional 
    path('api/tweets/', include('tweets.api.urls')),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    re_path(r'api/profiles?/', include('profiles.api.urls')),   # this will include url of api that we make for follow and unfollow
    
]

# settings.DEBUG is true then take the given urls
if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, 
                    document_root=settings.STATIC_ROOT)




