
import logging
from ....imports.views_imports import *


logger = logging.getLogger(__name__)

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Album]: # type: ignore
        logger.debug("get_queryset method called")
        if isinstance(self.request.user, (AbstractBaseUser, AnonymousUser)):
            logger.debug(f"Filtering albums for user: {self.request.user}")
            return self.queryset.filter(user=self.request.user)
        logger.debug("No valid user found, returning empty queryset")
        return Album.objects.none()

    def perform_create(self, serializer):
        logger.debug("perform_create method called")
        if isinstance(self.request.user, AbstractBaseUser):
            logger.debug(f"Creating album for user: {self.request.user}")
            serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        logger.debug("update method called")
        album = self.get_object()
        if album.user != request.user:
            logger.warning(f"User {request.user} attempted to edit album owned by {album.user}")
            raise PermissionDenied("You do not have permission to edit this album.")
        logger.debug(f"Album updated for user: {request.user}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug("destroy method called")
        album = self.get_object()
        if album.user != request.user:
            logger.warning(f"User {request.user} attempted to delete album owned by {album.user}")
            raise PermissionDenied("You do not have permission to delete this album.")
        logger.debug(f"Album deleted for user: {request.user}")
        return super().destroy(request, *args, **kwargs)
