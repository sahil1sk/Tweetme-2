from django.shortcuts import render, redirect
from django.conf import settings # we import this for get allowed hosts
# Http404 means page not found
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from .models import Tweet
import random
from .forms import TweetForm
from django.utils.http import is_safe_url   # here we importing the safe url for checking the url is safe
from .serializers import TweetSerializer    # here we importing the TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view # importing decorators

# we take the allowed hosts here from settings
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# here we normally show the data
def home_view(request, *args, **kwargs):
    #return HttpResponse("Hello World")
    return render(request, "pages/home.html", context={}, status=200)



# here we create this function using rest_frame work for creating tweets this method we call internally by javascript
@api_view(['POST']) # here in the list we allow which method will accept this function so here we allow POST
def tweet_create_view(request, *args, **kwargs):
    if request.method == "POST":
        serializer = TweetSerializer(data = request.POST)    # data is required to pass in the serializer    
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=201)        # we are using Response in serializer because it will send data in Json form
    return Response({}, status = 400)

# this function we make to get all the tweets using serializer this is called internally by javascript
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
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

