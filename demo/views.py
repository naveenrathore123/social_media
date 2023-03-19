from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment

from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer
)

User = get_user_model()

class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError('User not found')
        
        user = request.user
        if user == user_to_follow:
            raise ValidationError('Cannot follow yourself')

        user.follow(user_to_follow)
        return Response(status=status.HTTP_200_OK)

class UnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError('User not found')
        
        user = request.user
        if user == user_to_unfollow:
            raise ValidationError('Cannot unfollow yourself')

        user.unfollow(user_to_unfollow)
        return Response(status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(author=self.request.user, post=post)

class AllPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).order_by('-created_at')
