from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH # getting max tweet length from settings

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    # we will get the value for validation autmatically in serializer
    def validate_content(self, value):          # here we validate the data
        if len(value) > MAX_TWEET_LENGTH:
           raise serializers.ValidationError("This tweet is too long")    # if form length is greather than 250 characters than it will return the error otherwise retrurn the content
        return value
