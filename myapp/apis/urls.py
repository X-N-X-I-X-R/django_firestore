from myapp.logic.views.jitsimeet import MeetingViewSet
from myapp.logic.views.main_logic import AlbumViewSet, ImagesViewSet
from myapp.models.UserprofileFolder.userprofile_model import Album
from ..imports.urls_imports import *
from rest_framework import routers

admin_router = routers.DefaultRouter()

# Create a new router for the posts URLs
posts_router = routers.DefaultRouter()
posts_router.register(r'likes', LikeViewSet)
posts_router.register(r'comments', CommentViewSet)

# Register the other viewsets with the main router
router = routers.DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'userprofile', UserProfileViewSet, basename='userprofile')

router.register(r'posts', PostViewSet, basename='user-post')
router.register(r'follows', FollowViewSet, basename='user-follow')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'activitylogs', ActivityLogViewSet, basename='activitylogs')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'meetings', MeetingViewSet)
router.register(r'images', ImagesViewSet, basename='images')
router.register(r'albums', AlbumViewSet , basename='albums')


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', AutenticacionTokenView.as_view(), name='login'),
    path('api/register_user/', UserViewSet.as_view({'post': 'register', 'put': 'create'}), name='create_user'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api/posts/', include(posts_router.urls)),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# from rest_framework import routers
# from django.urls import path, include, re_path
# from rest_framework_simplejwt.views import TokenRefreshView
# from ..logic.views.Aut_Token import AutenticacionTokenView, LogoutView  
# from django.conf import settings
# from django.conf.urls.static import static
# from myapp.logic.views.users_viewset  import UserViewSet, UserProfileViewSet, PostViewSet, CommentViewSet, LikeViewSet, FollowViewSet, NotificationViewSet, ActivityLogViewSet, MessageViewSet,ActivateAccount
# from django.contrib.auth import views as auth_views



# # Create a new router for the posts URLs
# posts_router = routers.DefaultRouter()
# posts_router.register(r'likes', LikeViewSet)
# posts_router.register(r'comments', CommentViewSet)

# # Register the other viewsets with the main router
# router = routers.DefaultRouter()
# router.register(r'profiles', UserProfileViewSet, basename='profiles')
# router.register(r'posts', PostViewSet, basename='user-post')
# router.register(r'follows', FollowViewSet, basename='user-follow')
# router.register(r'notifications', NotificationViewSet, basename='notifications')
# router.register(r'activitylogs', ActivityLogViewSet, basename='activitylogs')
# router.register(r'messages', MessageViewSet, basename='messages')
# # router.register(r'users', UserViewSet, basename='users')  
# router.register(r'search', UserProfileViewSet, basename='search') 



# urlpatterns = [
#     path('login/', AutenticacionTokenView.as_view(), ),
#     path('api/register_user/', UserViewSet.as_view({'post': 'register', 'put': 'create'}), name='create_user'),  
#     path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#     path('logout', LogoutView.as_view(), name='logout'),
#     path('api/', include(router.urls)),
#     path('api/posts/', include(posts_router.urls)), 
    
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


#     path('activate/', ActivateAccount.as_view(), name='activate'),
# ]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# # Full paths for all URLs:
# # http://localhost:8000/login
# # http://localhost:8000/login/refresh
# # http://localhost:8000/logout
# # http://localhost:8000/register
# # http://localhost:8000/api/profiles/
# # http://localhost:8000/api/profiles/<int:pk>/follow
# #/api/profiles/create_user.
# # http://localhost:8000/api/posts/
# # http://localhost:8000/api/posts/likes/
# # http://localhost:8000/api/posts/comments/
# # http://localhost:8000/api/follows/


# # If in DEBUG mode:
# # http://localhost:8000/media/images/my_image.jpg.
    
    
    
