from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .tasks import send_welcome_email

@receiver(post_save, sender=CustomUser)
def post_user_create_signal(sender, instance, created, **kwargs):
    print("helooo")
    if created:
        send_welcome_email(instance.email, instance.username)
