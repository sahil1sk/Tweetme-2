from django import forms
from .models import Tweet
from django.conf import settings


MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH    # here we are getting max tweet length from the settings 

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
    
    def clean_content(self):                # function we make for validating the data
        content = self.cleaned_data.get("content") # getting the clean data
        if len(content) > MAX_TWEET_LENGTH:
           raise forms.ValidationError("This tweet is too long")    # if form length is greather than 250 characters than it will return the error otherwise retrurn the content
        return content

