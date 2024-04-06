from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from myapp.logic.views.users_viewset import ActivityLogViewSet, CommentViewSet, FollowViewSet, LikeViewSet, MessageViewSet, NotificationViewSet, PostViewSet, RegisterViewSet, UserProfileViewSet, UserViewSet
from .logic.views.Aut_Token import AutenticacionTokenView, LogoutView  
from django.conf import settings
from django.conf.urls.static import static




'''
This code defines the URL routing for a Django application. We're using Django Rest Framework's routers to automatically generate URLs for our viewsets. We create two routers: one for posts-related URLs and one for the rest. We register our viewsets with the routers, specifying a URL prefix for each one. We also add a custom route for the 'follow' action in UserProfileViewSet. Finally, we define the URLs for login, logout, register, and the API endpoints. If DEBUG is enabled, we also add a URL pattern for serving media files.

'''

'''
FOR All Api's  ---->>>   Swagger   ==   (http://localhost:8000/swagger/ )  -- > project/urls.py   
'''



# Create a new router for the posts URLs
posts_router = routers.DefaultRouter()
posts_router.register(r'likes', LikeViewSet)
posts_router.register(r'comments', CommentViewSet)

# Register the other viewsets with the main router
router = routers.DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'posts', PostViewSet, basename='user-post')
router.register(r'follows', FollowViewSet, basename='user-follow')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'activitylogs', ActivityLogViewSet, basename='activitylogs')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'users', UserViewSet, basename='users')  
router.register(r'search', UserProfileViewSet, basename='search') 
router.register(r'register_user', RegisterViewSet, basename='create_user')


urlpatterns = [
    path('login', AutenticacionTokenView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('api/posts/', include(posts_router.urls)),  # Include the posts URLs

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# Full paths for all URLs:
# http://localhost:8000/login
# http://localhost:8000/login/refresh
# http://localhost:8000/logout
# http://localhost:8000/register
# http://localhost:8000/api/profiles/
# http://localhost:8000/api/profiles/<int:pk>/follow
#/api/profiles/create_user.
# http://localhost:8000/api/posts/
# http://localhost:8000/api/posts/likes/
# http://localhost:8000/api/posts/comments/
# http://localhost:8000/api/follows/


# If in DEBUG mode:
# http://localhost:8000/media/images/my_image.jpg.
    
    
    
