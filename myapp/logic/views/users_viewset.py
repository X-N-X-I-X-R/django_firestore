




# import json
# from django.http import HttpResponse, JsonResponse
# from sqlalchemy import true
# from myapp.imports.views_imports import *

# from myapp.logic.convert_complex_data.serializers import *



# logger = logging.getLogger(__name__)

# def send_activation_email(user, request):
#     refresh = AutenticacionToken.get_token(user)
#     refresh_token = str(refresh)
#     current_site = get_current_site(request)
#     mail_subject = 'Activate your account'
#     message = render_to_string('acc_active_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#         'refresh_token': refresh_token,
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
    
#     logger.debug("Attempting to send email to %s", user.email)
#     try:
#         email = EmailMessage(
#             mail_subject,
#             message,
#             'the-farm@outlook.co.il',
#             [user.email],
#         )
#         email.content_subtype = "html"  # this is the crucial line
#         email.send()
#         logger.debug("Email sent to %s", user.email)
#     except Exception as e:
#         logger.error("Error sending email: %s", e)

# def activate_account(request):
#     key = request.GET.get('key')
#     try:
#         activation_email = ActivateAccount_Email.objects.get(activation_key=key, is_active=False)
#         activation_email.activate_account()
#         activation_email.user.is_active = True
#         activation_email.user.save()
#         activation_email.save()
#         logger.info("Account activated for user: %s", activation_email.user.email)
#         return redirect('login')  # Redirect to login page after activation
#     except ActivateAccount_Email.DoesNotExist:
#         logger.error("Activation failed for key: %s", key)
#         return redirect('error')  # Redirect to an error page if activation fails

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     def get_serializer_class(self):
#         if self.action == 'register':
#             return RegisterSerializer
#         return UserProfileSerializer
    
#     @action(detail=False, methods=['post'])
#     def register(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = User.objects.create_user(
#                 username=serializer.validated_data['username'],
#                 email=serializer.validated_data['email'],
#                 password=serializer.validated_data['password'],
#                 is_active=False  # Set the user as inactive until email verification
#             )
#             # Avoid sending another email in create method
#             send_activation_email(user, request)
#             return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         user = User.objects.get(id=response.data['id']) # type: ignore
#         # Generate activation key and send activation email
#         activation_email = ActivateAccount_Email(user=user)
#         activation_email.generate_activation_key()
#         activation_email.save()
#         return response  # Return the response object instead of None

#     @action(detail=False, methods=['post'])
#     def login_view(request):
#         data = json.loads(request.body) # type: ignore
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             try:
#                 activation_email = ActivateAccount_Email.objects.get(is_active=True, user=user)
#             except ActivateAccount_Email.DoesNotExist:
#                 return JsonResponse({"message": "Activation email does not exist for this user."}, status=400)
#             if activation_email.is_active:
#                 login(request, user)
#                 return JsonResponse({"message": "Logged in successfully."}, status=200)
#             else:
#                 return JsonResponse({"message": "Your account is not activated. Please check your email for the activation link."}, status=400)
#         else:
#             return JsonResponse({"message": "Invalid login credentials."}, status=400)



# class ActivateAccount(APIView):
#     def get(self, request):
#         key = request.GET.get('key', default=None)
#         if key is None:
#             # Handle the case where 'key' parameter is missing
#             return redirect('http://localhost:4200/home')
        
#         try:
#             activation_email = ActivateAccount_Email.objects.get(activation_key=key, is_active=False)
#             activation_email.activate_account()
#             activation_email.user.is_active = True
#             activation_email.user.save()
#             activation_email.save()
#             # Redirect to your frontend activation success page
#             return redirect('http://localhost:4200/home/')
#         except ActivateAccount_Email.DoesNotExist:
#             # Redirect to your frontend activation failure page
#             return redirect('http://localhost:4200/market-data')


# class UserProfileViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = UserProfile.objects.all()
#         serializer = UserProfileSerializers(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         try:
#             user_profile = UserProfile.objects.get(pk=pk)
#             serializer = UserProfileSerializers(user_profile)
#             return Response(serializer.data)
#         except UserProfile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def create(self, request):
#         serializer = UserProfileSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk=None):
#         try:
#             user_profile = UserProfile.objects.get(pk=pk)
#             serializer = UserProfileSerializer(user_profile, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except UserProfile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def destroy(self, request, *args, **kwargs):
#         try:
#             user_profile = UserProfile.objects.get(pk=kwargs['pk'])
#             user_profile.active = False
#             user_profile.save()
#             return Response({"message": "The profile has been removed."}, status=status.HTTP_200_OK)
#         except UserProfile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)


# ##########################
    
# class PostViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing posts.
#     """
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single post by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new post.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing post.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a post.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CommentViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing comments.
#     """
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single comment by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new comment.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing comment.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a comment.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class LikeViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing likes.
#     """
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single like by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new like.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing like.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a like.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class FollowViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and following users.
#     """
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single follow by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new follow.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing follow.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Unfollow a user.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class NotificationViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing notifications.
#     """
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single notification by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new notification.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing notification.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a notification.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ActivityLogViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing activity logs.
#     """
#     queryset = ActivityLog.objects.all()
#     serializer_class = ActivityLogSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single activity log by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new activity log.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing activity log.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete an activity log.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class MessageViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing and editing messages.
#     """
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializers

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a single message by its id.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new message.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing message.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a message.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    
