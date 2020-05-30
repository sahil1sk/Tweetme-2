from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet                   # We importing model for testing
from rest_framework.test import APIClient   # we importing API CLIENT

# In this File we basically test the model everything is working correctly or not
# for run the test use "python manage.py test"

# Create your tests here.
User = get_user_model()   # here we are getting the user model  to create user

                                    # NOTE_IMPORTANT
                                    # the tweet which will create in another function not in setUp will not remain at the end of the task 
                                    # the tweet will be deleted after that function is completed so if you want that the tweet that you create must remain at last then create in setUp

class TweetTestCase(TestCase):
    # setUp is the built in method which allows to create the user
    def setUp(self):                                                        # create many user as we need                         
        user = User.objects.create_user(username="cfe", password="somepassword")   # here we creating the user and we are also able to 
        user2 =  User.objects.create_user(username="sahil", password="password")
        Tweet.objects.create(content="My First tweet", user=user)
        Tweet.objects.create(content="My Second tweet", user=user2)           

    def test_user_created(self):          # here we are testing the user created or not
        user = User.objects.get(username="cfe")
        self.assertEqual(user.username, "cfe")         # assert will check the username is equal to cfe if yes then this line is pass otherwise not
               
                                                                          
    def test_tweet_created(self):
        user = User.objects.get(username = "cfe")
        tweet_obj = Tweet.objects.create(content="My Third tweet", user=user)
        self.assertEqual(tweet_obj.id, 3)           # here we check tweet_obj.id is equal to 3 or not because total 3 tweets are there                          
        self.assertEqual(tweet_obj.user, user)      # here we see username is equal to user or not

    # SO NOW WE ARE GOING TO TEST OUR API URL

    # so here in this method we will test the user that we created that login successfully
    #def test_api_login(self):
    #    user = User.objects.get(username = "cfe")
    #    client = APIClient()
    #    client.login(username=user.username, password='somepassword')

    #this method we use to get the client which we login    
    def get_client(self):
        user = User.objects.get(username = "cfe")
        client = APIClient()
        client.login(username=user.username, password='somepassword')
        return client       # after login we will return the client


    # so here we test our url which provide the list of api
    def test_tweet_list(self):
        client = self.get_client()              # getting the client from the function to get the login client
        response = client.get("/api/tweets/")       # here login client will send the request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),2)      # here we see lenth of tweet is 2 because we create 2 tweets in setUp function the other tweet we create in test_tweet_created after that function that tweet will automatically destroyed so length is 2
        print(response.json())

    # here we creating this method for checking the action like
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"like"})
        self.assertEqual(response.status_code, 200)
        
        like_count = response.json().get("likes") # so here we getting the likes
        self.assertEqual(like_count, 1)
        print(response.json())

    # here we creating this method for checking the action unlike
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"unlike"})
        self.assertEqual(response.status_code, 200)
        
        like_count = response.json().get("likes") # so here we getting the likes
        self.assertEqual(like_count,0)
        print(response.json())

    # here we creting this method for checking the action retweet
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(1,new_tweet_id)  # so here this means retweet_id will be different than the id which we give means 1

    # this method is used to check that the new tweet is created successfully
    def test_tweet_create_api_view(self):
        data = {"content": "this is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", data)
        self.assertEqual(response.status_code, 201)
        print(response.json())

    # this method we make to test the detail url     
    def test_tweet_detail_api_view(self):   
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    # this method we make to check the delete url is working properly    
    def test_tweet_delete_api_view(self):
        client = self.get_client()                                              
        response = client.delete("/api/tweets/1/delete/")       # deleting the id
        self.assertEqual(response.status_code, 200)
        
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")   # again deleting that id then we will get the error
        self.assertEqual(response.status_code, 404)
        
        client = self.get_client()
        response = client.delete("/api/tweets/2/delete/")   # again deleting the tweet with id 2 that is created by another user as you see above in setUp function 
        print("Here is the delete: ",response.json())       # so it will send code 401 means the login user is not able to delete the tweet which is created by other user
        self.assertEqual(response.status_code, 401)
        
      
        