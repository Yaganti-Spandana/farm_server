from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_url = f"http://localhost:3000/reset-password/{reset_password_token.key}"

    send_mail(
        subject="Password Reset for Dairy Farm",
        message=f"Use this link to reset your password:\n{reset_url}",
        from_email="yaganti06@gmail.com",
        recipient_list=[reset_password_token.user.email],
    )