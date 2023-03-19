from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views

urlpatterns = [
    path('api/authenticate/', obtain_jwt_token),
    path('api/token-refresh/', refresh_jwt_token),
    path('api/token-verify/', verify_jwt_token),
    path('api/follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('api/unfollow/<int:user_id>/', views.UnfollowView.as_view(), name='unfollow'),
    path('api/user/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/posts/', views.CreatePostView.as_view(), name='create-post'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/comment/', views.CommentView.as_view(), name='comment'),
    path('api/all_posts/', views.AllPostsView.as_view(), name='all-posts'),
]
