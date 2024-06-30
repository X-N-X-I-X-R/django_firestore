import logging
from ....imports.views_imports import *

logger = logging.getLogger(__name__)

class AutenticacionToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        logger.debug(f"Getting token for user: {user.username}")
        print(colored('Getting token for user: ' + user.username, 'green'))
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        token['last_login'] = user.last_login.isoformat() if user.last_login else None
        token['id'] = user.id
        token['groups'] = [group.name for group in user.groups.all()]
        token['username'] = user.username
        token['email'] = user.email
        token['created_token_time'] = token['iat']
        token['time_to_expired'] = token['exp']
        token['user_permissions'] = [perm.codename for perm in user.user_permissions.all()]
        token['user_nickname'] = user.userprofile.user_nickname if hasattr(user, 'userprofile') else None
        token['user_profile_id'] = user.userprofile.id if hasattr(user, 'userprofile') else None

        if user.is_superuser:
            token['user_permissions'] = "The king, All permissions Allow"
        else:
            permissions = user.user_permissions.all()
            token['user_permissions'] = ', '.join(perm.codename for perm in permissions)
            print(colored('User permissions: ' + token['user_permissions'], 'green'))
            logger.debug(f"User permissions: {token['user_permissions']}")

        return token

class AutenticacionTokenView(TokenObtainPairView):
    serializer_class = AutenticacionToken

    def post(self, request, *args, **kwargs):
        logger.debug("TokenObtainPairView POST request received")
        response = super().post(request, *args, **kwargs)
        logger.debug(f"Token generated for user: {request.data.get('username', 'unknown')}") # type: ignore
        return response
