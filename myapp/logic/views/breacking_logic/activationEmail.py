from myapp.logic.views.breacking_logic.customToken import AutenticacionToken
from ....imports.views_imports import * 


logger = logging.getLogger(__name__)

def send_activation_email(user, request):
    refresh = AutenticacionToken.get_token(user)
    refresh_token = str(refresh)
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'refresh_token': refresh_token,
        'protocol': 'https' if request.is_secure() else 'http'
    })

    logger.debug("Attempting to send email to %s", user.email)
    try:
        email_host_user = config('EMAIL_HOST_USER')
        if not isinstance(email_host_user, str):
            raise ValueError("EMAIL_HOST_USER must be a string.")
        
        email = EmailMessage(
            mail_subject,
            message,
            email_host_user,
            [user.email],
        )
        email.content_subtype = "html"
        email.send()
        logger.debug("Email sent to %s", user.email)
    except Exception as e:
        logger.error("Error sending email: %s", e)



class ActivateAccount(APIView):
    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64)) # type: ignore
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            activation_email = ActivateAccount_Email.objects.get(user=user)
            activation_email.activate_account()
            activation_email.save()
            return redirect('http://localhost:5173/login')
        else:
            return redirect('http://localhost:5173/register')
