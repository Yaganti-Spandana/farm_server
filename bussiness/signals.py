# bussiness/signals.py

import os
import logging
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Sends a password reset email via SendGrid API when a reset token is created.
    """
    try:
        # Construct the password reset URL
        reset_url = f"https://farm-dairy.netlify.app/reset-password/{reset_password_token.key}"

        # Email content
        subject = "Password Reset for Dairy Farm"
        html_content = f"""
        <p>Hello {reset_password_token.user.username},</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request this, please ignore this email.</p>
        """

        # Send the email using SendGrid API
        message = Mail(
            from_email=os.environ.get("DEFAULT_FROM_EMAIL", "yagantispandana@gmail.com"),
            to_emails=reset_password_token.user.email,
            subject=subject,
            html_content=html_content
        )

        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)

        # Optional: log success for debugging
        logger.info(
            f"Password reset email sent to {reset_password_token.user.email}, "
            f"status_code={response.status_code}"
        )

    except Exception as e:
        # Log errors without crashing the server
        logger.error(f"Failed to send password reset email to {reset_password_token.user.email}: {e}")