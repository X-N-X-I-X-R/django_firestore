from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from myapp.logic.views.main_logic import UserViewSet, UserProfileViewSet, PostViewSet, CommentViewSet, LikeViewSet, FollowViewSet, NotificationViewSet, ActivityLogViewSet, MessageViewSet,ActivateAccount
from myapp.logic.views.main_logic import AutenticacionTokenView, LogoutView



imports =[ 
  DefaultRouter, path, TokenRefreshView, settings, auth_views, static, include, LikeViewSet, CommentViewSet, AutenticacionTokenView, LogoutView, ActivateAccount, UserViewSet, UserProfileViewSet, PostViewSet, FollowViewSet, NotificationViewSet, ActivityLogViewSet, MessageViewSet
]
