from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
logger.error(f"EMAIL USER: {settings.EMAIL_HOST_USER}")
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        reset_url = f"https://farm-dairy.netlify.app/reset-password/{reset_password_token.key}"

        send_mail(
            subject="Password Reset for Dairy Farm",
            message=f"Use this link to reset your password:\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reset_password_token.user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Password reset email failed: {e}")