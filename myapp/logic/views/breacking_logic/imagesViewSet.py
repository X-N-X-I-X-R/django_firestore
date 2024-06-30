from pydantic import ValidationError
from ....imports.views_imports import *
from rest_framework.parsers import MultiPartParser, FormParser
from ...convert_complex_data.serializers import ImageSerializer
import logging

logger = logging.getLogger(__name__)
class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.order_by('album_id')
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[Images]: # type: ignore
        logger.debug("get_queryset called")
        if hasattr(self.request.user, 'userprofile'):
            user_profile = self.request.user.userprofile  # type: ignore
            logger.debug(f"Fetching images for user profile: {user_profile}")
            return self.queryset.filter(user=user_profile)
        logger.debug("User is not authenticated or has no user profile")
        return Images.objects.none()

    def perform_create(self, serializer):
        logger.debug("perform_create called with data: %s", self.request.data)  # type: ignore
        required_fields = ['user_image_container', 'image_subject', 'album']
        for field in required_fields:
            if field not in self.request.data:  # type: ignore
                raise ValidationError(f'{field} is required')
        if hasattr(self.request.user, 'userprofile'):
            user_profile = self.request.user.userprofile  # type: ignore
            album_id = self.request.data.get('album')  # type: ignore
            if not album_id:
                raise ValidationError('Album ID is required')
            try:
                album = Album.objects.get(id=album_id)
            except Album.DoesNotExist:
                raise ValidationError('Invalid album ID')
            logger.debug(f"Creating image for user profile: {user_profile}")
            serializer.save(user=user_profile, album=album)
            
    def update(self, request, *args, **kwargs):
        logger.debug("update called")
        image = self.get_object()
        if image.user != request.user.userprofile:
            logger.warning("User does not have permission to edit this image")
            raise PermissionDenied("You do not have permission to edit this image.")
        logger.debug(f"Updating image for user profile: {request.user.userprofile}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug("destroy called")
        image = self.get_object()
        if image.user != request.user.userprofile:
            logger.warning("User does not have permission to delete this image")
            raise PermissionDenied("You do not have permission to delete this image.")
        logger.debug(f"Deleting image for user profile: {request.user.userprofile}")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def set_profile_picture(self, request, pk=None):
        logger.debug("set_profile_picture called")
        image = self.get_object()
        if image.user != request.user.userprofile:
            logger.warning("User does not have permission to set this image as profile picture")
            raise PermissionDenied("You do not have permission to set this image as profile picture.")
        user = request.user.userprofile
        logger.debug(f"Setting profile picture for user profile: {user}")
        user.images.update(is_profile_picture=False)
        image.is_profile_picture = True
        image.save()
        return Response({'status': 'profile picture set'})
