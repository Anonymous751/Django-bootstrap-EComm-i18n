from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from .tokens import account_activation_token

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)

        activate_url = f"{settings.SITE_URL}{reverse('accounts:activate', kwargs={'uidb64':uidb64, 'token':token})}"

        subject = "Activate your account"
        message_plain = f"Please click the link to activate your account: {activate_url}"
        message_html = f"<p>Please click the link to activate your account:</p><p><a href='{activate_url}'>Activate</a></p>"

        email = EmailMultiAlternatives(
            subject,
            message_plain,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email]
        )
        email.attach_alternative(message_html, "text/html")
        email.send()