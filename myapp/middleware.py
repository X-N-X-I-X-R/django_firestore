import logging
from typing import Callable
from functools import wraps

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import resolve
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request

logger = logging.getLogger(__name__)

class APIMiddleware:
    """
    Middleware for handling API requests, authentication, and documentation access.
    
    Features:
    - Authentication required for all endpoints including Swagger
    - Developer role check for API documentation
    - Request logging
    - API version validation
    - Error handling
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        
        # Define paths that don't require authentication
        self.public_paths = {
            '/api/v1/auth/login/',
            '/api/v1/auth/register/',
            '/api/v1/auth/token/',
            '/api/v1/auth/token/refresh/',
            '/api/v1/verify-email/',
            '/api/v1/register/customer/',
            '/api/v1/register/advisor/',
            '/static/',
            '/media/',
        }
        
        # Define paths that require developer role
        self.developer_paths = {
            '/swagger/',
            '/redoc/',
            '/api/schema/'
        }
        
        # Define allowed API versions
        self.allowed_versions = {'v1'}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Handle the request through the middleware."""
        try:
            # Add request ID for tracking
            request.id = self._generate_request_id()
            
            # Log the incoming request
            self._log_request(request)
            
            # Skip authentication checks for public paths
            if self._is_public_path(request.path):
                return self.get_response(request)
                
            # Skip API authentication for admin paths
            if request.path.startswith('/admin/'):
                return self.get_response(request)
            
            # For API paths, check authentication
            if request.path.startswith('/api/'):
                # Check authentication
                if not self._is_authenticated(request):
                    return JsonResponse({
                        'error': 'Authentication required',
                        'detail': 'Please log in to access this resource'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                # Check if user is active
                if not self._is_user_active(request):
                    return JsonResponse({
                        'error': 'Account not activated',
                        'detail': 'Please check your email to activate your account'
                    }, status=status.HTTP_403_FORBIDDEN)
            
            # Check developer role for API documentation
            if self._is_developer_path(request.path) and not self._is_developer(request):
                return JsonResponse({
                    'error': 'Developer access required',
                    'detail': 'You need developer privileges to access the API documentation'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Process the request
            response = self.get_response(request)
            
            # Log the response
            self._log_response(request, response)
            
            return response
            
        except Exception as e:
            logger.exception(f'Error processing request: {str(e)}')
            return JsonResponse({
                'error': 'Internal server error',
                'request_id': getattr(request, 'id', None)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_request_id(self) -> str:
        """Generate a unique ID for request tracking."""
        import uuid
        return str(uuid.uuid4())

    def _is_public_path(self, path: str) -> bool:
        """Check if the path is public (doesn't require authentication)."""
        # Remove trailing slash for consistency
        path = path.rstrip('/')
        
        # Special handling for static and media files
        if path.startswith('/static') or path.startswith('/media'):
            return True
            
        # Check other public paths
        for public_path in self.public_paths:
            public_path = public_path.rstrip('/')
            if path == public_path or path.startswith(public_path + '/'):
                return True
        return False

    def _is_developer_path(self, path: str) -> bool:
        """Check if the path is for API documentation."""
        return any(path.startswith(dev_path) for dev_path in self.developer_paths)

    def _is_developer(self, request: HttpRequest) -> bool:
        """
        Check if the user has developer privileges.
        Developer is either a staff member or has the 'developer' group.
        """
        if not self._is_authenticated(request):
            return False
        
        user = request.user
        return user.is_staff or user.groups.filter(name='developer').exists()

    def _validate_api_version(self, request: HttpRequest) -> bool:
        """Validate the API version in the request path."""
        try:
            parts = request.path.split('/')
            if 'api' in parts:
                idx = parts.index('api')
                if len(parts) > idx + 1:
                    version = parts[idx + 1]
                    return version in self.allowed_versions
            return False
        except Exception:
            return False

    def _is_authenticated(self, request: HttpRequest) -> bool:
        """Check if the request is authenticated."""
        return request.user and request.user.is_authenticated

    def _is_user_active(self, request: HttpRequest) -> bool:
        """Check if the authenticated user is active."""
        return request.user.is_active if self._is_authenticated(request) else False

    def _log_request(self, request: HttpRequest) -> None:
        """Log incoming request details."""
        logger.info(
            f'Request {request.id}: {request.method} {request.path} '
            f'from {request.META.get("REMOTE_ADDR")} '
            f'user: {request.user if request.user.is_authenticated else "anonymous"}'
        )

    def _log_response(self, request: HttpRequest, response: HttpResponse) -> None:
        """Log response details."""
        logger.info(
            f'Response {request.id}: {response.status_code} '
            f'for {request.method} {request.path}'
        )


# Settings for Swagger UI customization
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'OPERATIONS_SORTER': 'method',
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch',
    ],
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'none',
    'DEFAULT_MODEL_RENDERING': 'model',
    'DEEP_LINKING': True,
    'DISPLAY_OPERATION_ID': False,
    'DEFAULT_MODEL_DEPTH': 3,
} 