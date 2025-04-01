from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class SwaggerLoginView(View):
    template_name = 'swagger/swagger_login.html'

    def get(self, request):
        # If user is already authenticated and has proper permissions
        if request.user.is_authenticated:
            logger.info(f"User {request.user.email} is authenticated. Staff: {request.user.is_staff}, Superuser: {request.user.is_superuser}")
            if request.user.is_staff or request.user.is_superuser:
                next_url = request.GET.get('next', 'schema-swagger-ui')
                return redirect(next_url)
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        logger.info(f"Login attempt for email: {email}")
        
        try:
            user = User.objects.get(email=email)
            logger.info(f"Found user: {user.email}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
            
            # Try authenticating with both email and username
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is None:
                user_auth = authenticate(request, email=email, password=password)
            
            logger.info(f"Authentication result: {'Success' if user_auth else 'Failed'}")
            
        except User.DoesNotExist:
            logger.warning(f"User with email {email} not found")
            user_auth = None
        
        if user_auth is not None and (user_auth.is_staff or user_auth.is_superuser):
            login(request, user_auth)
            logger.info(f"Successfully logged in user: {user_auth.email}")
            next_url = request.GET.get('next', 'schema-swagger-ui')
            return redirect(next_url)
        else:
            if user_auth is None:
                logger.warning("Authentication failed")
                messages.error(request, 'Invalid credentials')
            else:
                logger.warning(f"User {email} lacks required permissions")
                messages.error(request, 'Insufficient permissions. Staff or admin access required.')
            return render(request, self.template_name)

def staff_member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempting to access staff-only view")
            return redirect(f"{reverse('swagger-login')}?next={request.path}")
        if not (request.user.is_staff or request.user.is_superuser):
            logger.warning(f"Non-staff user {request.user.email} attempting to access staff-only view")
            messages.error(request, 'Staff or admin access required')
            return redirect('swagger-login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
