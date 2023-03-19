from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['user', 'followers_count', 'following_count']
        
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'author', 'created_at', 'comments_count', 'likes_count']
        
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
