import logging
from ....imports.views_imports import *

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    def post(self, request):
        logger.debug("Logout request received")
        refresh_token = request.data.get("refresh_token")

        if refresh_token is None:
            logger.error("Refresh token is required")
            print(colored('Refresh token is required', 'red'))
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.debug("Token blacklisted successfully")
        except TokenError:
            logger.error("Invalid token")
            print(colored('Invalid token', 'red'))
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        print(colored('Token blacklisted successfully', 'green'))
        return Response(status=status.HTTP_205_RESET_CONTENT)
