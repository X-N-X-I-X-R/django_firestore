/envelope/ HTTP/1.1" 200 2
INFO     2024-05-28 19:51:05 "POST /api/register_user/ HTTP/1.1" 201 76 from basehttp, line 212 in log_message
INFO:django.server:"POST /api/register_user/ HTTP/1.1" 201 76
INFO:root:Account activated for nirstam@gmail.com
INFO     2024-05-28 19:51:45 "GET /activate/?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcxMDIyNjMsImlhdCI6MTcxNjkyNTg2Mywic3ViIjoxMTd9.-QAffxClhaJV2NwpiWex4_qYkTM9fyKzCjdX7MARBTM HTTP/1.1" 302 0 from basehttp, line 212 in log_message
INFO:django.server:"GET /activate/?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcxMDIyNjMsImlhdCI6MTcxNjkyNTg2Mywic3ViIjoxMTd9.-QAffxClhaJV2NwpiWex4_qYkTM9fyKzCjdX7MARBTM HTTP/1.1" 302 0
WARNING  2024-05-28 19:51:59 Unauthorized: /login/ from log, line 241 in log_response
WARNING:django.request:Unauthorized: /login/
WARNING  2024-05-28 19:51:59 "POST /login/ HTTP/1.1" 401 63 from basehttp, line 212 in log_message
WARNING:django.server:"POST /login/ HTTP/1.1" 401 63
DEBUG:urllib3.connectionpool:https://o4507004549595136.ingest.us.sentry.io:443 "POST /api/4507004552282112/envelope/ HTTP/1.1" 200 2


#Make sure the ActivateAccount_Email model is correctly defined and its methods work as expected.
Ensure the email backend is properly configured in your Django settings.
Check that the activation endpoint (the one that handles the /activate/ URL) is correctly set up to activate users when provided with a valid activation key.
If you're testing this locally, make sure your email client isn't blocking emails from your local server.


def login_view(request): data = json.loads(request.body) username = data.get('username') password = data.get('password') user = authenticate(request, username=username, password=password) if user is not None: try: activation_email = ActivateAccount_Email.objects.get(user=user) except ActivateAccount_Email.DoesNotExist: return JsonResponse({"message": "Activation email does not exist for this user."}, status=400) if activation_email.is_active: login(request, user) return JsonResponse({"message": "Logged in successfully."}, status=200) else: return JsonResponse({"message": "Your account is not activated. Please check your email for the activation link."}, status=400) else: return JsonResponse({"message": "Invalid login credentials."}, status=400)

class ActivateAccount_Email(models.Model):
activation_id = models.AutoField(primary_key=True, help_text="The ID of the activation email.")
user = models.ForeignKey(User, on_delete=models.CASCADE)
activation_key = models.CharField(max_length=40, help_text="The activation key for the account.")
activation_date = models.DateTimeField(auto_now_add=True, help_text="The date when the activation email was sent.")
is_active = models.BooleanField(default=False, help_text="Check this if the account has been activated.")

def generate_activation_key(self):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=2, seconds=3600),
        'iat': datetime.now(timezone.utc),
        'sub': self.user.id # type: ignore
    }
    self.activation_key = jwt.encode(
        payload,
        'SECRET_KEY', # Replace with your SECRET_KEY
        algorithm='HS256'
    )
    self.save()
    
def activate_account(self):
    self.is_active = True
    logging.info(f"Account activated for {self.user.username}")
    return self.is_active

def get_activation_key(self):
    return self.activation_key  
logging.info(f"Activation key retrieved for user ")

def __str__(self):
    return f"{self.user.username}'s Activation Email"

    class ActivateAccount(APIView): def get(self, request): key = request.GET.get('key', default=None) if key is None: # Handle the case where 'key' parameter is missing return redirect('http://localhost:4200/login/')

        try:
        activation_email = ActivateAccount_Email.objects.get(activation_key=key, is_active=False)
        activation_email.activate_account()
        activation_email.user.is_active = True
        activation_email.user.save()
        activation_email.save()
        # Redirect to your frontend activation success page
        return redirect('http://localhost:4200/home')
    except ActivateAccount_Email.DoesNotExist:
        # Redirect to your frontend activation failure page
        return redirect('http://localhost:4200/market-data')


          def register(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_active=False  # Set the user as inactive until email verification
        )
        send_activation_email(user, request)
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    if 'id' in response.data: # type: ignore
        user = User.objects.get(id=response.data['id'])  # type: ignore
    else:
        # Handle the case when 'id' is not in response.data
        user = User.objects.get(username=response.data['username'])  # type: ignore
    

    class UserViewSet(viewsets.ModelViewSet):
queryset = User.objects.all()
serializer_class = RegisterSerializer

@action(detail=False, methods=['post'])
def register(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_active=False  # Set the user as inactive until email verification
        )
        send_activation_email(user, request)
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    if 'id' in response.data: # type: ignore
        user = User.objects.get(id=response.data['id'])  # type: ignore
    else:
        # Handle the case when 'id' is not in response.data
        user = User.objects.get(username=response.data['username'])  # type: ignore
    

    
    # Generate activation key and send activation email
    activation_email = ActivateAccount_Email(user=user)
    activation_email.generate_activation_key()
    activation_email.save()

    activation_link = f"{request.build_absolute_uri('/activate/')}?key={activation_email.activation_key}"
    send_mail(
        'Activate Your Account',
        f'Click the link to activate your account: {activation_link}',
        'the-farm@outlook.co.il',
        [user.email],
        fail_silently=False,
    )
    
    return response  # Return the response object instead of None


    def login_view(request): data = json.loads(request.body) username = data.get('username') password = data.get('password') user = authenticate(request, username=username, password=password) if user is not None: try: activation_email = ActivateAccount_Email.objects.get(user=user) except ActivateAccount_Email.DoesNotExist: return JsonResponse({"message": "Activation email does not exist for this user."}, status=400) if activation_email.is_active: login(request, user) return JsonResponse({"message": "Logged in successfully."}, status=200) else: return JsonResponse({"message": "Your account is not activated. Please check your email for the activation link."}, status=400) else: return JsonResponse({"message": "Invalid login credentials."}, status=400)

Check the login_view function to ensure it's correctly checking the is_active field of the ActivateAccount_Email associated with the user. Check the ActivateAccount view to ensure it's correctly setting the is_active field of the ActivateAccount_Email when the account is activated. Check the send_activation_email function and the register action in the UserViewSet to ensure they're correctly creating the ActivateAccount_Email and setting its is_active field. If all the above checks pass, there might be a problem with the data in the database. You might need to manually update the is_active field of the ActivateAccount_Email associated with the user to match the is_active

;"velmaliahmac-(main[]*[])-Django_server$:sqlite3 db.sqlite "SELECT * FROM myapp_activateaccount_email; 12|eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcxMDIyNjMsImlhdCI6MTcxNjkyNTg2Mywic3ViIjoxMTd9.-QAffxClhaJV2NwpiWex4_qYkTM9fyKzCjdX7MARBTM|2024-05-28 19:51:03.391348|1|117   