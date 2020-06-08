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

# so we upgrade this function we are able to use this function for getting profile and also for adding and removing follower
# this function will return the api which will give the detail related to the user which we will give
@api_view(['GET', 'POST'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail":"User not found"}, status=404)
    profile_obj = qs.first()
                                 # so here we also able to pass context in the serializer    we are also able to pass instance as well   
    
    if request.method == 'POST':  # so here we add request.method is post means now this api is called for adding or removing follower
        me = request.user
        data = request.data or {}
        action = data.get("action") 
        
        if profile_obj.user != me:                                    # you can also able to do in the given way            
            if action == "follow":              # if me in profile.followers.all(): 
                profile_obj.followers.add(me)       #   profile.followers.remove(me)
            elif action == "unfollow":          # else:
                profile_obj.followers.remove(me)    #   profile.followers.add(me)
            else:
                pass

    serializer = PublicProfileSerializer(instance=profile_obj, context={"request":request})    # so here we passing instance to get the data or to show data we are also able to do without adding instance      
    return Response(serializer.data, status=200)


# this function will help to add the follow and unfollow
#@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
#def user_follow_view(request, username, *args, **kwargs):
#    me = request.user
#    other_user_qs = User.objects.filter(username=username)
#    
#    if me.username == username:                             #  if the user is same then we normally return the count
#        my_followers = me.profile.followers.all()
#        return Response({"count": my_followers.count()}, status=200)
#    
#    if not other_user_qs.exists():
#        return Response({}, status=404)
#
#    other = other_user_qs.first()
#    profile = other.profile
#    data = request.data or {}
#    action = data.get("action") 
#                                        # you can also able to do in the given way            
#    if action == "follow":              # if me in profile.followers.all(): 
#        profile.followers.add(me)       #   profile.followers.remove(me)
#    elif action == "unfollow":          # else:
#        profile.followers.remove(me)    #   profile.followers.add(me)
#    else:
#        pass
#    
#    # so here we send the new data through serializer
#    data = PublicProfileSerializer(instance=profile, context={"request":request})                            # here we also return the count of the other profile while get method
#    return Response(data.data, status=200)
