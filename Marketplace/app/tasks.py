from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from .models import Cart


@shared_task
def send_welcome_email(user_email, user_name):
    subject = 'Welcome to Our Service'
    message = f'Hi {user_name}, thank you for registering at our site.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    print("emailsent")
    send_mail(subject, message, email_from, recipient_list)






@shared_task
def send_email_to_cart_owners():
    for cart in Cart.objects.exclude(cartproduct__isnull=True).distinct():
        print("cart")
        if cart.cartproduct_set.exists():  # Ensures the cart is not empty
            subject = "Reminder: You have items in your cart!"
            message = f"Hi {cart.user.username}, you have items waiting in your cart. Don't miss out!"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [cart.user.email]
            send_mail(subject, message, email_from, recipient_list)
