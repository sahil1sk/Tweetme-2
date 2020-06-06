from rest_framework import serializers
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count  = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "id",
            "bio",
            "location",
            "follower_count",
            "following_count",
            "is_following",
            "username",
        ]
 
    # this function will help to check the user who request the data follow this profile or not 
    def get_is_following(self, obj):
        is_following = False
        context = self.context        # this context we pass throgh profile/api/views
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()  # so here we get the user who fetch the data follow to profile or not
        return is_following

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username

    def get_following_count(self, obj):
        return obj.user.following.count() 

    def get_follower_count(self, obj):
        return obj.followers.count()
        # return obj.user.profile.follower.all() 
        