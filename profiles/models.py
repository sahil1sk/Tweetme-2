from django.db import models
from django.conf import settings
from django.db.models.signals import post_save # there are signal like pre_save, post_delete amd many more

User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)         # here we use onetoone field means one user have one profile
    location = models.CharField(max_length=220, null=True, blank=True)  # blank means not required by django null menas not required by database
    bio = models.TextField(blank=True, null=True)                           


# this function we create when any user will save in the database then it will create a profile for that user
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:                                                     # if the user is newly created then we will create it's profile                
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)           # this will check the new user will save or not


  