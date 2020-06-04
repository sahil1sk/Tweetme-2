        # IMP_NOTE THIS VIEWS INCLUDE ALL PURE DJANGO AND SERIALIZER URL

from django.shortcuts import render, redirect
from django.conf import settings # we import this for get allowed hosts
# Http404 means page not found
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from ..models import Tweet
import random
from ..forms import TweetForm
from django.utils.http import is_safe_url   # here we importing the safe url for checking the url is safe
from ..serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer)    # here we importing the TweetSerializer

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication # so here we importing session authentication 
from rest_framework.decorators import api_view, authentication_classes,permission_classes # importing decorators
from rest_framework.permissions import IsAuthenticated # here we importing the authentication premission
# we take the allowed hosts here from settings
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


# here we create this function using rest_frame work for creating tweets this method we call internally by javascript
# @authentication_classes([SessionAuthentication])  but this is built in permission_classes
@api_view(['POST']) # here in the list we allow which method will accept this function so here we allow POST
@permission_classes([IsAuthenticated])   # there we add premission that user must be autheticated
def tweet_create_view(request, *args, **kwargs):
    if request.method == "POST":            # data is required to pass in the serializer
        serializer = TweetCreateSerializer(data = request.data)        # we have to take it as request.data because we given json 
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=201)        # we are using Response in serializer because it will send data in Json form
    return Response({}, status = 400)

# this function we make to get all the tweets using serializer this is called internally by javascript
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')       # so this will fetch the username
    if username != None:                         # iexact will help if we get Justin but in the database having justin then it will return that name                                        
        qs = qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs, many=True)  # many to true menas many tweets are allowed
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  tweet_feed_view(request, *args, **kwargs):
    user = request.user
    profiles = user.following.all()     # getting the all users where our user objects is exists
    followed_users_id = []
    if profiles.exists():
        followed_users_id = [x.user.id for x in profiles]  # here we get the each userId to whom i follow
    followed_users_id.append(user.id)
    qs = Tweet.objects.filter(user__id__in = followed_users_id).order_by("-timestamp")  # so here we get all the tweets of the user to whom we followed using it's id
    serializer = TweetSerializer(qs, many=True)  # many to true menas many tweets are allowed
    return Response(serializer.data, status=200)


# so this funcion we use to get the data on that id which we pass
@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)     # 404 meas not found
    obj = qs.first()        # .first() means it will be the first element
    serializer = TweetSerializer(obj) # here we not use many true because it will be one  
    return Response(serializer.data, status=200)

# so here we make this function for deleting the tweet
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({"message":"Could not find the tweet"}, status=404)     # 404 meas not found
    qs = qs.filter(user=request.user)
    if not qs.exists(): # if the user is not exist in the user so he will not able to delete the tweet
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()        # here we get the tweet of first element
    obj.delete() # so here we will delete that tweet if the user is doing 
    return Response({"message":"Tweet removed"}, status=200)

# this method we make for adding and removing the like
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
  
    '''
        id is required
        Action options are: like, unlike, retweet
    '''
    # from home.html side we side the data in json form so for recieving
    # that data we have to use request.data instead of request.POST
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):      # if the data is valid then we do other things
        data = serializer.validated_data
        tweet_id = data.get("id")           # here we get the tweet id from validated data return by serializer
        action = data.get("action")         # getting the action
        content = data.get("content")       # getting the content from the serializer
    
        qs = Tweet.objects.filter(id=tweet_id)  # here we get the object where id is equal to the given id
        if not qs.exists():
            return Response({}, status=404)     # 404 meas not found
        obj = qs.first()        # here we get the tweet of first element

        if action == "like":            # so if the action is like then we add the like
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)         # here we will serialize the data  
            return Response(serializer.data, status=200)   # here we send the response  
        elif action == "unlike":        # if the action is unlike then we remove the like    
            obj.likes.remove(request.user)   
            serializer = TweetSerializer(obj) 
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                        user=request.user, 
                        parent = obj,
                        content = content) # here we creating the new tweet belong to this tweet as we use foreign key      

            serializer = TweetSerializer(new_tweet)       # here we serialize the tweet
            return Response(serializer.data, status=201)                                        

    return Response({"message":"something"}, status=200)


# this function is used to create the tweets
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)    # 401 means not authorized but it's always means that not authorized 
        return redirect(settings.LOGIN_URL)

    #print("ajax", request.is_ajax()) # so here it will give true or false this is ajax request or not
    if request.method == "POST":
        form = TweetForm(request.POST)
        next_url = request.POST.get('next')
        if form.is_valid():
            obj = form.save(commit=False)  # so here we make commit to false because we don't want to commit the changes now
            obj.user = user                 # in this line we add user
            obj.save()                      # so here we save the commit is automatically set to true if don't provide false

            if request.is_ajax():   # if it's ajax request then we will return json response othewise we will redirect where we want
                # obj.serialize() will help to send the data which we create now
                return JsonResponse(obj.serialize(), status=201) # 201 for created item

            if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS): # this will check if the url is safe checking the safe using hosts then redirect otherwise not
                return redirect(next_url)

        if form.errors:         # this if will check if there is any error
            if request.is_ajax():   # if the request is of ajax type the send error with JsonResponse
                return JsonResponse(form.errors, status=400)    # 400 means input mistake or some other mistake by user

    form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

# this function is called by the javascript internally to show all the tweets
def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()                                # here we creating the random likes between 0 to 124 for each    
    # x.serialize() function we call from the model.py file so we add the dictionary from there not from there to write whole code
    tweets_list = [x.serialize() for x in qs] # so here we add element in dict and then all elements using for loop we add in list
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

# this function is used to show the specific detail of the tweet using it's id
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    
    return JsonResponse(data, status=status)


