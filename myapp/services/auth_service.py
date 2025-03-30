from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.signing import TimestampSigner
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.log import setup_logger

logger = setup_logger(__name__)

class AuthService:
    @staticmethod
    def send_verification_email(user, verification_url, is_advisor=False):
        """Send verification email to user"""
        try:
            subject = 'Verify your email address'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            
            # Choose template based on user type
            template = 'registration/verify_email_advisor.html' if is_advisor else 'registration/verify_email.html'
            
            # Prepare context
            context = {
                'user': user,
                'verification_url': verification_url,
                'is_advisor': is_advisor
            }
            
            # Render HTML content
            html_content = render_to_string(template, context)
            text_content = strip_tags(html_content)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[to_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Verification email sent to {user.email}")
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
            raise

    @staticmethod
    def send_admin_notification(user, is_advisor=False):
        """Send notification to admin about new registration"""
        try:
            subject = f'New {"Advisor" if is_advisor else "Customer"} Registration'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = settings.ADMIN_EMAIL
            
            # Choose template based on user type
            template = 'registration/admin_notification.html' if is_advisor else 'registration/admin_new_customer.html'
            
            # Prepare context
            context = {
                'user': user,
                'is_advisor': is_advisor
            }
            
            # Render HTML content
            html_content = render_to_string(template, context)
            text_content = strip_tags(html_content)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[to_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Admin notification sent for new user: {user.email}")
            
        except Exception as e:
            logger.error(f"Failed to send admin notification for {user.email}: {str(e)}")
            raise

    @staticmethod
    def generate_verification_token(user):
        """Generate verification token for user"""
        try:
            signer = TimestampSigner()
            token = signer.sign(user.email)
            logger.info(f"Generated verification token for user: {user.email}")
            return token
        except Exception as e:
            logger.error(f"Failed to generate verification token for {user.email}: {str(e)}")
            raise

    @staticmethod
    def verify_token(token):
        """Verify token and return email"""
        try:
            signer = TimestampSigner()
            email = signer.unsign(token, max_age=86400)  # 24 hours
            logger.info(f"Token verified for email: {email}")
            return email
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise

    @staticmethod
    def generate_tokens(user):
        """Generate JWT tokens for user"""
        try:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            logger.info(f"Generated tokens for user: {user.email}")
            return tokens
        except Exception as e:
            logger.error(f"Failed to generate tokens for {user.email}: {str(e)}")
            raise

    @staticmethod
    def get_verification_url(request, token):
        """Generate verification URL"""
        try:
            verification_url = request.build_absolute_uri(f'/api/v1/verify-email/{token}/')
            logger.info(f"Generated verification URL for token: {token}")
            return verification_url
        except Exception as e:
            logger.error(f"Failed to generate verification URL: {str(e)}")
            raise 