from django.db import models
from django.conf import settings
from django.db.models.signals import post_save # there are signal like pre_save, post_delete amd many more

User = settings.AUTH_USER_MODEL

class FollowrRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)         # here we use onetoone field means one user have one profile
    location = models.CharField(max_length=220, null=True, blank=True)  # blank means not required by django null menas not required by database
    bio = models.TextField(blank=True, null=True)      
    timestamp = models.DateTimeField(auto_now_add=True)     # auto_now_add means when the profile is created               
    updated = models.DateTimeField(auto_now=True)           # recent update date
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    """
    project_obj = Profile.objects.first()
    project_obj.followers.all()          --> All users following this profile sara object de du jina eha profile ch na
    user.following.all()                 --> All users I follow   sara objects de du jitha vi apna user hega
    """

# this function we create when any user will save in the database then it will create a profile for that user
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:                                                     # if the user is newly created then we will create it's profile                
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)           # this will check the new user will save or not


  