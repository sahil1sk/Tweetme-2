import random
from django.db import models
from django.conf import settings

# so we are able to get the user from the settings from AUTH_USER_MODEL given is the way
# how to get user from the settings directly
User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    #user = model.ForeignKey(User, null=True, on_delete=models.SET_NULL) # this means on delete the user their tweet will not be deleted
    # when the user table will delete then all the tweets related to that user will be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True) # blank means not required in django null means not required in database
    
    def __str__(self):
        return self.content

    class Meta:             # here we define the meta so that we will order in reverse way
        ordering = ['-id']

    def serialize(self):    # here we make the normally function to send the data in the form of dictionary whenever we will call
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        } 

        