# bussiness/signals.py
from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.info(f"EMAIL USER: {settings.EMAIL_HOST_USER}")

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Sends password reset email using SendGrid verified sender.
    """
    try:
        # ✅ Use a verified sender email from SendGrid
        from_email = settings.DEFAULT_FROM_EMAIL

        # Construct reset URL (frontend should handle /reset-password/:token route)
        reset_url = f"https://farm-dairy.netlify.app/reset-password/{reset_password_token.key}"

        subject = "Password Reset for Dairy Farm"
        message = (
            f"Hello {reset_password_token.user.username},\n\n"
            f"You requested a password reset. Use the link below to reset your password:\n\n"
            f"{reset_url}\n\n"
            f"If you didn't request this, you can ignore this email.\n\n"
            f"Thanks,\nDairy Farm Team"
        )

        # Send email via SMTP (SendGrid)
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[reset_password_token.user.email],
            fail_silently=False,  # Raise exception if email fails
        )

        logger.info(f"Password reset email sent to {reset_password_token.user.email}")

    except Exception as e:
        # Log any exceptions
        logger.error(f"Password reset email failed for {reset_password_token.user.email}: {e}")