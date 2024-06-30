import logging
from ....imports.views_imports import *

logger = logging.getLogger(__name__)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        logger.debug("list method called")
        queryset = UserProfile.objects.filter(active=True)
        if request.user.is_authenticated:
            logger.debug(f"Authenticated user: {request.user}")
            queryset = queryset | UserProfile.objects.filter(user=request.user)
        serializer = UserProfileSerializer(queryset, many=True)
        logger.debug(f"Returning {len(serializer.data)} profiles")
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        logger.debug(f"retrieve method called with pk={pk}")
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            if user_profile.user != request.user and not user_profile.active:
                logger.warning("User does not have permission to view this profile")
                return Response({'detail': 'You do not have permission to view this profile.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = UserProfileSerializer(user_profile)
            logger.debug(f"Returning profile data for user {user_profile.user}")
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            logger.error("User profile not found")
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        logger.debug("create method called")
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug("Serializer is valid")
            serializer.save(user=request.user)
            logger.debug(f"User profile created for user {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.debug(f"update method called with pk={pk}")
        try:
            user_profile = UserProfile.objects.get(pk=pk, user=request.user)
            data = request.data.copy()
            if request.FILES.get('user_profile_image'):
                data['user_profile_image'] = request.FILES['user_profile_image']
            serializer = UserProfileSerializer(user_profile, data=data)
            if serializer.is_valid():
                logger.debug("Serializer is valid")
                serializer.save()
                logger.debug(f"User profile updated for user {request.user}")
                return Response(serializer.data)
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            logger.error("User profile not found")
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        logger.debug(f"destroy method called with pk={pk}")
        try:
            user_profile = UserProfile.objects.get(pk=pk, user=request.user)
            user_profile.active = False
            user_profile.save()
            logger.debug(f"User profile deactivated for user {request.user}")
            return Response({"message": "The profile has been deactivated."}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            logger.error("User profile not found")
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
