from rest_framework import serializers
from .models import Tweet
from django.conf import settings
import random

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH            # getting max tweet length from settings
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS    # getting the action options from settings

# there is normall seriallizer for performing actions like adding like unlike retweet 
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()     #so we are declaring here because we don't use any model
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False) # so this we add for retweeting because we need to add retweeting content

    # here in this function we are validating the action
    def validate_action(self, value):
        value = value.lower().strip()           # this will change the value into the lower case
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweet")
        return value

# this serializer is used to create the tweet 
class TweetCreateSerializer(serializers.ModelSerializer):
    # SerializerMethodField This is a read-only field. It gets its value by calling the method 
    likes =  serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count() 

    # we will get the value for validation autmatically in serializer
    def validate_content(self, value):          # here we validate the data
        if len(value) > MAX_TWEET_LENGTH:
           raise serializers.ValidationError("This tweet is too long")    # if form length is greather than 250 characters than it will return the error otherwise retrurn the content
        return value


# the given serializer we make only to read the data
class TweetSerializer(serializers.ModelSerializer):
    # SerializerMethodField This is a read-only field. It gets its value by calling the method 
    likes =  serializers.SerializerMethodField(read_only = True)
    parent = TweetCreateSerializer(read_only = True) # the data is not in the serializer form so that's why we will use TweetCreateSerializer to serialize the data
    #content = serializers.SerializerMethodField(read_only = True) # here we made this for get_content method to show the data

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', "parent"] # is_retweet provide true or false it is basically that function which we make in the model.py file under Tweet model so that why we are able to use this here

    def get_likes(self, obj):       # this function we make to count the likes
        return obj.likes.count() 

    # so here in this function we will send the content of the parent tweet if the tweet is retweeted
    '''
    def get_content(self, obj):
        content = obj.content
        if obj.is_retweet:
            content = obj.parent.content
        return content
    '''

