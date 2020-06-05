import random
from django.db import models
from django.conf import settings
from django.db.models import Q  # Q will help to perform more filter or more qurey in one time


# so we are able to get the user from the settings from AUTH_USER_MODEL given is the way
# how to get user from the settings directly
User = settings.AUTH_USER_MODEL

# through this table we add the like to tweet 
# this model we basically make when that like is added
class TweetLike(models.Model):   # the through is present in likes help to add data in this model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# so this class will in function when it is called by the tweetManager
class TweetQuerySet(models.QuerySet):
    # so from view we call this method to perform the action then Query set will perform the action only with that method
    def by_username(self, username):
        return self.filter(user__username__iexact = username)

    def feed(self, user):
        profiles = user.following.exists()     # where our user exists all that users will provided
        followed_users_id = []
        if profiles:                  # so here we are getting the id of that user to whom we follow in efficient way                  
            followed_users_id = user.following.values_list("user__id", flat=True)     

        # self is now Tweet.objects
        return self.filter(
                Q(user__id__in = followed_users_id) |
                Q(user=user) # so here this means that if there is our username then also return if i follow to i 
            ).distinct().order_by("-timestamp")  # the user to whom we followed we get there using it's id and also by checking our user object exists at there
    

# And then here we calling this class 
class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):               # so here we return the model data who  called tweet manager and return to query set
        return TweetQuerySet(self.model, using=self._db)
    
    # so when we make a feed here then the get_querset will return data related to that user only query_set will not return whole model
    def feed(self, user):                            
        return self.get_queryset().feed(user)


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
    
    objects = TweetManager()      # so here we adding TweetManager to used as query set which we do in the tweet_feed_view view

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

        
