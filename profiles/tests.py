from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Profile

            # IMP_NOTE for runing this test file only use "python manage.py test profiles"

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cfe", password="somepassword")   # here we creating the user and we are also able to 
        self.userb =  User.objects.create_user(username="sahil", password="password")

    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
    
    def test_following(self):
        first = self.user
        second = self.userb

        first.profile.followers.add(second)                     # added a user
        
        print(second.following.all())     # because of we add related name so use following otherwise we are able to second.follower_set.all() # means where this user exists count that and give that set
        second_user_following_whom = second.following.all()     # here we get all the following     
        qs = second_user_following_whom.filter(user=first)      # here we filter from it following username first
        self.assertTrue(qs.exists())                            # if it's exist assert will true    

        first_user_following_no_one = first.following.all()     # so here we get all the following of first
        self.assertFalse(first_user_following_no_one.exists())  # but we don't add anyone so assertFalse will be true and test will be passed
