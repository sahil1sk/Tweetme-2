import random
from django.db import models
from django.conf import settings

# so we are able to get the user from the settings from AUTH_USER_MODEL given is the way
# how to get user from the settings directly
User = settings.AUTH_USER_MODEL

# through this table we add the like to tweet 
# this model we basically make when that like is added
class TweetLike(models.Model):   # the through is present in likes help to add data in this model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    # user = model.ForeignKey(User, null=True, on_delete=models.SET_NULL) # this means on delete the user their tweet will not be deleted

    # with the help of parent we will create a new tweet every time belong to the tweet
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL) # self menas that refence to this model 

    # related name will provide functionality like "user = User.objects.get('sahil')" 
    # user.tweets.all() this will provide all the tweets of user 
    # otherwise we have to use like user.tweet_set.all() if we don't have related name tweet

    # when the user table will delete then all the tweets related to that user will be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")    # throug TweetLike we are able to add manytomany field    # use the link for more understanding of through https://riptutorial.com/django/example/7838/with-a-through-model                
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)  # manytomany one user have many tweet(means like here) and many user having many tweet 
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True) # blank means not required in django null means not required in database
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #def __str__(self):
     #   return self.content

    class Meta:             # here we define the meta so that we will order in reverse way
        ordering = ['-id']

    @property                       # so here we make a method help to check it's tweet or retweet    
    def is_retweet(self):           # the basic logic is that if the parent is None then it's a retweet otherwise it is a tweet
        return self.parent != None

    def serialize(self):    # here we make the normally function to send the data in the form of dictionary whenever we will call
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        } 

        
