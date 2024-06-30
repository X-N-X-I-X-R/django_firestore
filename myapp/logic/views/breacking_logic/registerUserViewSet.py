import logging
from ....imports.views_imports import *

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_serializer_class(self) -> Type[Serializer]: # type: ignore
        logger.debug("get_serializer_class method called")
        if self.action == 'register':
            logger.debug("Action is 'register', using RegisterSerializer")
            return RegisterSerializer
        logger.debug("Using UserProfileSerializer")
        return UserProfileSerializer
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        logger.debug("register method called")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.debug("Serializer is valid")
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False  # Set the user as inactive until email verification
            )
            send_activation_email(user, request)
            logger.debug(f"User created and activation email sent to {user.email}")
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        logger.debug("create method called")
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id']) # type: ignore
        activation_email = ActivateAccount_Email(user=user)
        activation_email.generate_activation_key()
        activation_email.save()
        logger.debug(f"Activation email created for user {user.username}")
        return response
