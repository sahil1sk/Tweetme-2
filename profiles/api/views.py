import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# this function will return the api which will give the detail related to the user which we will give
@api_view(['GET'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail":"User not found"}, status=404)
    profile_obj = qs.first()
                                 # so here we also able to pass context in the serializer    we are also able to pass instance as well   
    data = PublicProfileSerializer(instance=profile_obj, context={"request":request})    # so here we passing instance to get the data or to show data we are also able to do without adding instance
    return Response(data.data, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username)
    
    if me.username == username:                             #  if the user is same then we normally return the count
        my_followers = me.profile.followers.all()
        return Response({"count": my_followers.count()}, status=200)
    
    if not other_user_qs.exists():
        return Response({}, status=404)

    other = other_user_qs.first()
    profile = other.profile
    data = request.data or {}
    action = data.get("action") 
                                        # you can also able to do in the given way            
    if action == "follow":              # if me in profile.followers.all(): 
        profile.followers.add(me)       #   profile.followers.remove(me)
    elif action == "unfollow":          # else:
        profile.followers.remove(me)    #   profile.followers.add(me)
    else:
        pass
    
    current_followers_qs = profile.followers.all()                                  # here we also return the count of the other profile while get method
    return Response({"count": current_followers_qs.count()}, status=200)