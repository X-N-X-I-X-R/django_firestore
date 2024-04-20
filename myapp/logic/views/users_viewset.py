from myapp.imports.views_imports import *
from myapp.logic.convert_complex_data.serializers import *





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AutUser
    
    


class UserProfileViewSet(viewsets.ViewSet):
    """
    A ViewSet for viewing and editing user profiles.
    """

    def list(self, request):
        """
        List all user profiles.
        """
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single user profile by its id.
        """
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Create a new user profile.
        """
        serializer = UserProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an existing user profile.
        """
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Deactivate the user account.
        """
        try:
            user_profile = UserProfile.objects.get(pk=kwargs['pk'])
            user_profile.active = True
            user_profile.save()
            return Response({"message": "The profile has been removed."}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PostViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing posts.
    """


    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single post by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new post.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing post.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a post.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single comment by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new comment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing comment.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a comment.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing likes.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single like by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new like.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing like.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a like.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and following users.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single follow by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new follow.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing follow.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Unfollow a user.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single notification by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new notification.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing notification.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a notification.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityLogViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing activity logs.
    """
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single activity log by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new activity log.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing activity log.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an activity log.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single message by its id.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# Viewset for user registration and email verification 
class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create a new User instance
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False  # User is not active until email is validated
            )
            # Save the User instance
            user.save()

            # Generate a token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh)

            # Generate a validation link
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            abs_url = 'http://'+current_site+relative_link+"?token="+access_token

            # Send a validation email
            send_mail(
                'Verify your email',
                'Hi '+user.username+', use the link below to verify your email \n' + abs_url,
                'noreply@mywebsite.com',
                [user.email],
                fail_silently=False,
            )

            # Use the Firestore client
            try:
                fire_fire_db(fire_db)
            except ValueError as e:
                print(e)

            # Return a successful response with the created User instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return a 400 Bad Request response with the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
